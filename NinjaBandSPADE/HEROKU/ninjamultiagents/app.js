
/**
 * Module dependencies.
 */
//IP address of the SPADE MAS 
var spade_ip = "http://192.168.0.100:8008"; //Comment/uncomment depending on the network the system is running -> Home
//var spade_ip = "http://10.13.91.8:8008"   //Comment/uncomment depending on the network the system is running -> ITESM

 // Include our ninja-blocks library
var ninjaBlocks = require('ninja-blocks');

// Instantiate a ninja object with your API token from https://a.ninja.is/hacking
var ninja = ninjaBlocks.app({user_access_token:"10aeda14a8dd4da3b3df52e55c9f8c9268c9bcae"});

var my_device = "1313BB000464_0_0_11"; //RF
var ninja_eyes= "1313BB000464_0_0_1007";
var temperature_sensor="1313BB000464_0101_0_31";
var turn_on_ID = "000001111010000100100000";
var turn_off_ID = "000001111010000100100001";
var turn_onL0 = "000001111010000100100010";
var turn_onL1 = "000001111010000100100011";
var turn_onL2 = "000001111010000100100100";
var turn_onL3_25 = "000001111010000100100101";
var turn_onL3_50 = "000001111010000100100110";
var turn_onL3_75 = "000001111010000100100111";
var turn_onL3_100 = "000001111010000100101000";
var turn_off_all = "000001111010000100101001";

//******************************************
var my_subdevice = "000000011101010100110000"; // 24bit string specifying the red button
var HOSTNAME = "http://ninjamultiagents.herokuapp.com";	// For example http://mycoolapp.herokuapp.com
//ninja.device(ninja_eyes).subscribe(HOSTNAME+'/white_eyes',true,function(err){}); 
//ninja.device(my_device).unsubscribe(function(err) {})  //Function to unsubscribe from a device
//ninja.device(my_device).subscribe(spade_ip,true,function(err){});     // Note that route 'rf' is arbitrary but informative.
//ninja.device(my_device).subscribe(HOSTNAME+'/pink_eyes',true,function(err){}); 

var express = require('express');
var routes = require('./routes');
var user = require('./routes/user');
var http = require('http');
var path = require('path');
var _ = require('underscore');

var app = express();


// all environments
app.set('port', process.env.PORT || 3000); //Set Ports
app.set('views', path.join(__dirname, 'views')); //Tells the app where to find its views
app.set('view engine', 'jade'); //Tell the app which engine to render the views
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(app.router);
app.use(require('stylus').middleware(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

//Tell the server what to do if there's a get to the specified direction
app.get('/', routes.index);
app.get('/users', user.list);


//Post to turn the light ON
app.post('/turn_on' , function(req, res){
  handleSubscription_turn_on(req.body.DA,res);
});

  //Post to turn the light OFF
app.post('/turn_off' , function(req, res){
  handleSubscription_turn_off(req.body.DA,res);});
  
app.post('/turn_onL0' , function(req, res){
  handleSubscription_turn_onL0(req.body.DA,res);});

app.post('/turn_onL1' , function(req, res){
  handleSubscription_turn_onL1(req.body.DA,res);});

app.post('/turn_onL2' , function(req, res){
  handleSubscription_turn_onL2(req.body.DA,res);});

app.post('/turn_onL3_0' , function(req, res){
  handleSubscription_turn_onL3_0(req.body.DA,res);});

app.post('/turn_onL3_1' , function(req, res){
  handleSubscription_turn_onL3_1(req.body.DA,res);});

app.post('/turn_onL3_2' , function(req, res){
  handleSubscription_turn_onL3_2(req.body.DA,res);});

app.post('/turn_onL3_3' , function(req, res){
  handleSubscription_turn_onL3_3(req.body.DA,res);});

app.post('/turn_off_all' , function(req, res){
  handleSubscription_turn_off_all(req.body.DA,res);});
/*
  var options = {
  hostname: '192.168.1.110',
  port: 8005,
  path: '/posted',
  method: 'POST'
};

var requ = http.request(options, function(resp) {
  console.log('STATUS: ' + resp.statusCode);
  console.log('HEADERS: ' + JSON.stringify(resp.headers));
  resp.setEncoding('utf8');
  resp.on('data', function (chunk) {
    console.log('BODY: ' + chunk);
  });
});

requ.on('error', function(e) {
  console.log('problem with request: ' + e.message);
});

// write data to request body
requ.write('data\n');
requ.end();*/


//Post to send the temperature of the sensor
app.post('/req_temp' , function(req, res){
  handleSubscription_req_temp(req.body.DA,res);
});

//Post when the button is pressed
app.post('/rf' , function(req, res){
  console.log("Subdevice: " + my_subdevice);
  console.log("req.body.DA: " + req.body.DA);
  // This route will be hit when *any* RF433MHz signal is received.
  handleSubscription(req.body.DA);
  res.send(200);
});


// Implement a function to handle the receipt of the data
function handleSubscription_blu_eyes(guid, res) {
    console.log("Actuate Blue Eyes");
    ninja.devices({ device_type: 'temperature' }, function(err, devices) {
    _.each(devices, function(device,guid){
        ninja.device(guid).last_heartbeat(function(err, data) { 
            console.log(device.shortName+' is '+data.DA+'C');
            if(data.DA>=20 ){res.send(200, 'Sorry, cant turn Ninjas eyes blue because the temperature is: '+data.DA+'C');}
            else{
              ninja.device(ninja_eyes).actuate(blue1);
              res.send(200, 'Actuated, current temperature is: '+data.DA+'C');}
        })
    })
});
}


// Implement a function to handle the color swap of the ninja's eyes
function handleSubscription(guid) {
    if (guid == my_subdevice) {
    console.log("The button was pressed");
    ninja.devices({ device_type: 'temperature' }, function(err, devices) {
    _.each(devices, function(device,guid){
        ninja.device(guid).last_heartbeat(function(err, data) { 
            console.log(device.shortName+' is '+data.DA+'C');
            if(data.DA<16 ){ninja.device(ninja_eyes).actuate(gren_eyes);} 
            if(data.DA>=16 && data.DA<17 ){ninja.device(ninja_eyes).actuate(blue1);} 
            if(data.DA>=17 && data.DA<18 ){ninja.device(ninja_eyes).actuate(blue2);} 
            if(data.DA>=18 && data.DA<19 ){ninja.device(ninja_eyes).actuate(blue3);} 
            if(data.DA>=19 && data.DA<20 ){ninja.device(ninja_eyes).actuate(blue4);} 
            if(data.DA>=20 && data.DA<21 ){ninja.device(ninja_eyes).actuate(green1);} 
            if(data.DA>=21 && data.DA<22 ){ninja.device(ninja_eyes).actuate(green2);} 
            if(data.DA>=22 && data.DA<23 ){ninja.device(ninja_eyes).actuate(green3);} 
            if(data.DA>=23 && data.DA<24 ){ninja.device(ninja_eyes).actuate(green4);} 
            if(data.DA>=24 && data.DA<25 ){ninja.device(ninja_eyes).actuate(orange1);} 
            if(data.DA>=25 && data.DA<26 ){ninja.device(ninja_eyes).actuate(orange2);} 
            if(data.DA>=26){ninja.device(ninja_eyes).actuate(red);} 
        })
    })
});
}}

// Implement a function to handle the receipt of the data
function handleSubscription_white_eyes(guid,res) {
    console.log("Actuate White Eyes");
    ninja.device(ninja_eyes).actuate(white);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_on(guid,res) {
    console.log("Turning the light on");
    ninja.device(my_device).actuate(turn_on_ID);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_onL0(guid,res) {
    console.log("Turning the light bulb on (L0)");
    ninja.device(my_device).actuate(turn_onL0);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_onL1(guid,res) {
    console.log("Turning the lamp on (L1)");
    ninja.device(my_device).actuate(turn_onL1);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_onL2(guid,res) {
    console.log("Turning the lamp on (L2)");
    ninja.device(my_device).actuate(turn_onL2);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_onL3_0(guid,res) {
    console.log("Turning the lamp on (L3) 25 percent");
    ninja.device(my_device).actuate(turn_onL3_25);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_onL3_1(guid,res) {
    console.log("Turning the lamp on (L3) 50 percent");
    ninja.device(my_device).actuate(turn_onL3_50);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_onL3_2(guid,res) {
    console.log("Turning the lamp on (L3) 75 percent");
    ninja.device(my_device).actuate(turn_onL3_75);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_onL3_3(guid,res) {
    console.log("Turning the lamp on (L3) 100 percent");
    ninja.device(my_device).actuate(turn_onL3_100);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_off(guid,res) {
    console.log("Turning the light on");
    ninja.device(my_device).actuate(turn_off_ID);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_turn_off_all(guid,res) {
    console.log("Turning the lights off");
    ninja.device(my_device).actuate(turn_off_all);
    res.send(200)
}


// Implement a function to handle the receipt of the data
function handleSubscription_req_temp(guid, res) {
    console.log("Sending temperature");
    ninja.devices({ device_type: 'temperature' }, function(err, devices) {
    _.each(devices, function(device,guid){
        ninja.device(guid).last_heartbeat(function(err, data) { 
            console.log(device.shortName+' is '+data.DA+'C');
            res.send(200, ''+data.DA);
        })
    })
});
}


//Create a running HTTP server
http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
