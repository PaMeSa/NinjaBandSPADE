
/**
 * Module dependencies.
 */

 // Include our ninja-blocks library
var ninjaBlocks = require('ninja-blocks');

// Instantiate a ninja object with your API token from https://a.ninja.is/hacking
var ninja = ninjaBlocks.app({user_access_token:"10aeda14a8dd4da3b3df52e55c9f8c9268c9bcae"});

var my_device = "1313BB000464_0_0_11"; //RF
var ninja_eyes= "1313BB000464_0_0_1007";
var temperature_sensor="1313BB000464_0101_0_31";
//Definition of colors for the ninja's eyes
var blue1 = "1D00FF"; 
var blue2 = "003FFF"; 
var blue3 = "00A2FF"; 
var blue4 = "00FFFF"; 
var green1 = "00FF9D"; 
var green2 = "00FF40";
var green3 = "22FF00";
var green4 = "80FF00";
var yellow = "E2FF00";
var orange1 = "FFBF00";
var orange2 = "FF5D00";
var red = "FF0000";
var pink = "FF0062";
var black = "000000";
var white = "FFFFFF";
//******************************************
var my_subdevice = "000000011101010100110000"; // 24bit string specifying the red button
var HOSTNAME = "http://ninja-xgame.herokuapp.com";	// For example http://mycoolapp.herokuapp.com
//ninja.device(ninja_eyes).subscribe(HOSTNAME+'/gren_eyes',true,function(err){}); 
//ninja.device(ninja_eyes).subscribe(HOSTNAME+'/blu_eyes',true,function(err){}); 
//ninja.device(ninja_eyes).subscribe(HOSTNAME+'/pink_eyes',true,function(err){}); 
//ninja.device(ninja_eyes).subscribe(HOSTNAME+'/black_eyes',true,function(err){}); 
//ninja.device(ninja_eyes).subscribe(HOSTNAME+'/white_eyes',true,function(err){}); 
//ninja.device(my_device).unsubscribe(function(err) {})  //Function to unsubscribe from a device
//ninja.device(my_device).subscribe('http://187.138.99.67:8005/',true,function(err){});     // Note that route 'rf' is arbitrary but informative.
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


//Post to turn the ninjas eyes green
app.post('/gren_eyes' , function(req, res){
  handleSubscription_gren_eyes(req.body.DA,res);
});

//Post to turn the ninjas eyes blue
app.post('/blu_eyes' , function(req, res){
  handleSubscription_blu_eyes(req.body.DA,res);
});

//Post to turn the ninjas eyes white
app.post('/white_eyes' , function(req, res){
  handleSubscription_white_eyes(req.body.DA,res);
});

//Post to turn the ninjas eyes pink
app.post('/pink_eyes' , function(req, res){
  handleSubscription_pink_eyes(req.body.DA,res);
  
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
});

//Post to turn the ninjas eyes black
app.post('/black_eyes' , function(req, res){
  handleSubscription_black_eyes(req.body.DA,res);
});

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

// Implement a function to handle the receipt of the data
function handleSubscription_gren_eyes(guid, res) {
    console.log("Actuate Green Eyes");
    ninja.devices({ device_type: 'temperature' }, function(err, devices) {
    _.each(devices, function(device,guid){
        ninja.device(guid).last_heartbeat(function(err, data) { 
            console.log(device.shortName+' is '+data.DA+'C');
            if(data.DA<=20 ){res.send(200, 'Sorry, cant turn Ninjas eyes geen because the temperature is: '+data.DA+'C');}
            else{
              ninja.device(ninja_eyes).actuate(green3);
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
function handleSubscription_pink_eyes(guid,res) {
    console.log("Actuate Pink Eyes");
    ninja.device(ninja_eyes).actuate(pink);
    res.send(200)
}

// Implement a function to handle the receipt of the data
function handleSubscription_black_eyes(guid,res) {
    console.log("Actuate Black Eyes");
    ninja.device(ninja_eyes).actuate(black);
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
