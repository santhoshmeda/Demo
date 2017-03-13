$(document).ready(function() {

  // global arrays needed to buffer data points across events
  var env_table_data = [];
  var env_chart_data = [];
  var pre_table_data = [];
  // var pre_chart_data = [];
  var led1;
  var led2;
  var led3;
  // the key event receiver function
  iotSource.onmessage = function(e) {
    // must convert all single quoted data with double quote format
    // console.log(e.data);
    var double_quote_formatted_data = e.data.replace(/'/g, '"');
    // now we can parse into JSON
    // console.log(double_quote_formatted_data);
    parsed_json_data = JSON.parse(double_quote_formatted_data);
    console.log(parsed_json_data);
    clearEnvTables();
    clearPrTables();
    updateEnvironmentalTableData(parsed_json_data);
    updateEnvironChartData(parsed_json_data);    
    updatePressureTableData(parsed_json_data);
    updateStepperMotor(parsed_json_data);
    updateLeds(1,parsed_json_data['led_states']['led_red'])
    updateLeds(2,parsed_json_data['led_states']['led_grn'])
    updateLeds(3,parsed_json_data['led_states']['led_blu'])
  }

  // Buttons
  $('#motor_start').click(function() {
    console.log('Start Motor Up!');
    $.get('/motor/1');
  });

  $('#motor_stop').click(function() {
    console.log('Stop Motor');
    $.get('/motor/0');
  });

  $('#motor_zero').click(function() {
    console.log('Zero Motor Position');
    $.get('/motor_zero');
  });

  $('#motor_multistep').click(function() {
    var params = 'steps='+$('#motor_steps').val()+"&direction="+$('#motor_direction').val();
    console.log('Multistep with params:' + params);
    $.post('/motor_multistep', params, function(data, status){
                console.log("Data: " + data + "\nStatus: " + status);
                  });
  });


  // Text Fields
  $('#motor_speed').change(function() {
    console.log('Changed motor speed to ' + $('#motor_speed').val());
    $.get('/motor_speed/'+$('#motor_speed').val());
  });

  $('#motor_position').change(function() {
    console.log('Changed motor position to ' + $('#motor_position').val());
    $.get('/motor_position/'+$('#motor_position').val());
  });

  $('#motor_steps').change(function() {
    console.log('Changed motor steps to ' + $('#motor_steps').val());
    $.get('/motor_steps/'+$('#motor_steps').val());
  });

  $('#motor_direction').change(function() {
    console.log('Changed motor steps to ' + $('#motor_direction').val());
    $.get('/motor_direction/'+$('#motor_direction').val());
  });


  // ============================ STEPPER MOTOR ===============================
  function updateStepperMotor(data) {
    $('#motor_position').text(data['motor']['position']);
    if (data['motor']['state'] === '1') {
      $('#motor_state').toggleClass('label-default', false);
      $('#motor_state').toggleClass('label-success', true);
    } else if (data['motor']['state'] === '0') {
      $('#motor_state').toggleClass('label-default', true);
      $('#motor_state').toggleClass('label-success', false);
    }
  }
  // ============================ STEPPER MOTOR ===============================

  // ============================ DATE FUNCTIONS ==============================
  // previous lab
  function zeropad(num, size) {
      var s = "000000000" + num;
      return s.substr(s.length-size);
  }

  // ============================== ENV TABLE =================================
  updateEnvironmentalTableData = (function (d) {
    env_table_data.push(d);
    if (env_table_data.length > 4) {
      env_table_data.shift();
      clearEnvTables();
      }
      updateEnvironmentalTable(env_table_data);
  });

  function updateEnvironmentalTable(data) {
    $('tr.env-param-row').each(function(i) {
      temp_far = ((data[i]['environmental']['temperature']['reading']) * (9.0/5.0)) + 32
      var tm = '<td>' + data[i]['timestamp'] + '</td>';
      var t = '<td>' + data[i]['environmental']['temperature'].reading.toFixed(2) + '</td>';
      var p = '<td>' + temp_far.toFixed(2) + '</td>';
      $(this).append(tm);
      $(this).append(t);
      $(this).append(p);
    });
  }
  // ============================ENV Chart Data ================================
  function clearEnvTables() {
    $('tr.env-param-row').each(function(i) {
      $(this).empty();
    });
  }

  // Renders the jQuery-ui elements
  $("#tabs").tabs();

  var env_chart = new Morris.Line({
    element: 'temp-chart',
    data:[
    ],
    xkey: 'time',
    ykeys:['h'],
    labels:['%RH']
  });

  //build the chart data
  function updateEnvironChartData (json_obj) {
    env_chart_data.push(json_obj);
    if (env_chart_data.length >16) {
      env_chart_data.shift();
    }
    updateEnvironChart(env_chart_data);
  }

  //update the Chart
  function updateEnvironChart(data) {
    var chart_data = [];
    data.forEach(function(d) {
      env_record = {
        time: d['timestamp'],
        h: d['environmental']['temperature'].reading.toFixed(2)
      };
      chart_data.push(env_record);
      // console.log(env_record);
    });
    // console.log(env_chart);
    env_chart.setData(chart_data);
  }

  // =================Pressure Table =================================
  function clearPrTables() {
    $('tr.pressure-param-row').each(function(i) {
      $(this).empty();
    });
  }
  updatePressureTableData = (function (d) {
    pre_table_data.push(d);
    if (pre_table_data.length > 4) {
      pre_table_data.shift();
      clearEnvTables();
      }
      updatePressureTable(pre_table_data);
  });

  function updatePressureTable(data) {
    $('tr.pressure-param-row').each(function(i) {
      // temp_far = ((data[i]['environmental']['temperature']['reading']) * (9.0/5.0)) + 32
      var tm = '<td>' + data[i]['timestamp'] + '</td>';
      var t = '<td>' + data[i]['environmental']['pressure'].reading.toFixed(2) + '</td>';
      // var p = '<td>' + temp_far.toFixed(2) + '</td>';
      $(this).append(tm);
      $(this).append(t);
      // $(this).append(p);
    });
  }
  // ===================================================================
  // RED LED SLIDER
  $( "#slider1" ).slider({
    orientation: "vertical",
    range: "min",
    min: 0,
    max: 100,
    value: 50,
    animate: true,
    slide: function( event, ui ) {
      $( "#pwm1" ).val( ui.value );
      $.get('/led_red/' + $("#pwm1").val());
      // console.log("red led duty cycle(%):",ui.value);
    }
  });

  $( "#pwm1" ).val( $( "#slider1" ).slider( "value" ) );
  $("#pwm1").change(function() {
    console.log('LED RED Changed to' + $("#pwm1").val());
    $.get('/led_red/' + $("#pwm1").val());
    });
  // ===================================================================
  // GREEN LED SLIDER
  $( "#slider2" ).slider({
    orientation: "vertical",
    range: "min",
    min: 0,
    max: 100,
    value: 50,
    animate: true,
    slide: function( event, ui ) {
      $( "#pwm2" ).val( ui.value );
      $.get('/led_green/' + $("#pwm2").val());
      // console.log("grn led duty cycle(%):",ui.value);
    }
  });
  $( "#pwm2" ).val( $( "#slider2" ).slider( "value" ) );
    $('#pwm2').change(function() {
      console.log('LED GREEN Changed to' + $("#pwm2").val());
      $.get('/led_green/' + $("#pwm2").val());
    });


    /* update the LEDs based on their SSE state monitor */
    function updateLeds(ledNum, ledValue) {
      // console.log(ledNum,ledValue);
      if (ledNum === 1) {
        if (ledValue === 1) {
          $('#red_led_label').toggleClass('label-danger', true);
          // $('#red_led_label').text('ON');
          // console.log('Inside Red Led (true)');
          led1 = "ON";
        } else if (ledValue === 0) {
          $('#red_led_label').toggleClass('label-danger', false);
          // $('#red_led_label').text('OFF');
          // console.log('Inside Red Led (false)');
          led1 = "OFF";
        }
      } else if (ledNum === 2) {
        if (ledValue === 1) {
          $('#grn_led_label').toggleClass('label-success', true);
          // $('#grn_led_label').text('ON');
          led2 = "ON";
        } else if (ledValue === 0) {
          $('#grn_led_label').toggleClass('label-success', false);
          // $('#grn_led_label').text('OFF');
          led2 = "OFF";
        }
      } else if (ledNum === 3) {
        if (ledValue === 1) {
          $('#blu_led_label').toggleClass('label-primary', true);
          // $('#blu_led_label').text('ON');
          console.log('Inside Blu Led (true)');
          led3 = "ON";
        } else if (ledValue === 0) {
          $('#blu_led_label').toggleClass('label-primary', false);
          // $('#blu_led_label').text('OFF');
          led3 = "OFF";
        }
      }
    }

    // // make sure to intialize synchronously (10ms back to back)
// initial_conditions().then(led_status);
// The button click functions run asynchronously in the browser
$('#red_led_btn').click(function() {
  if (led1 === "OFF") {
    led1 = "ON";
  } else {
    led1 = "OFF";
  }
  var params = 'led=1&state=' + led1;
  console.log('Led Command with params:' + params);
  $.post('/ledcmd', params, function(data, status) {
    console.log("Data: " + data + "\nStatus: " + status);
  });
});

$('#grn_led_btn').click(function() {
  if (led2 === "OFF") {
    led2 = "ON";
  } else {
    led2 = "OFF";
  }
  var params = 'led=2&state=' + led2;
  console.log('Led Command with params:' + params);
  $.post('/ledcmd', params, function(data, status) {
    console.log("Data: " + data + "\nStatus: " + status);
  });
});

$('#blu_led_btn').click(function() {
  if (led3 === "OFF") {
    led3 = "ON";
  } else {
    led3 = "OFF";
  }
  var params = 'led=3&state=' + led3;
  console.log('Led Command with params:' + params);
  $.post('/ledcmd', params, function(data, status) {
    console.log("Data: " + data + "\nStatus: " + status);
  });
});


});
