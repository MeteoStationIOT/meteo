/* Ce code est une tentative de match up pour envoyer les éléments recus sur la socket */
var mqtt = require('mqtt');
var url = require('url');
var fs = require('fs');
var http = require('http');
var io = require('socket.io');

/* Dans cette partie, le serveur est crée et envoie un message sur une webSocket */
/***************************************************************************************************/
/* On crée le serveur http qui va communiquer avec le navigateur web */
var server = http.createServer(function(req, res){
  /* On récupère l'url sur laquelle le client s'est connectée */
  var url_request = req.url.toString();
  console.log(url_request); 

  if (url_request.length == 1 && url_request.includes('/') == true ){
    /* Au lancement du serveur, on charge le fichier sur lequel on va travailler */
    fs.readFile('./acceuil.html', 'utf-8', function(error, content){
      res.writeHead(200, {"Content-Type":"text/html"});
      res.end(content);
    });
  }

  else if (url_request.includes('/exterieure') == true){
    fs.readFile('./exterieur.html', 'utf-8', function(error, content){
      res.writeHead(200, {"Content-Type":"text/html"});
      res.end(content);
    });
  }
  
  else {
    res.end("pas encore implémenté"); 
  }


});

/* On met le serveur à l'écoute sur le port 8080 de notre machine */
server.listen(8080);

/* Gestion de l'evènement de connection, sans quoi aucun client ne peut se connecter */
  /* On met d'abord le serveur à l'écoute des connections webSockets */
var webSocket = io.listen(server);
  /* On gère ensuite l'evènement de connection sur cette nouvelle socket */
webSocket.on('connection', function(socket){
  /* On écrit sur la socket un message au client. Syntaxe('id_msg', 'msg') */
  webSocket.emit('slt', 'bonjour_client');
});
/***************************************************************************************************/


/* Dans cette partie, le serveur joue le role de client et recoit des données du cloud mqtt (broker) */
/***************************************************************************************************/ 
//Parse
var mqtt_url = url.parse(process.env.CLOUDMQTT_URL || 'mqtt://hrrgcrqx:af3wqGskmMfY@m20.cloudmqtt.com:12771');
var auth = (mqtt_url.auth || ':').split(':');
var url = "mqtt://" + mqtt_url.host;

var options = {
  port: mqtt_url.port,
  clientId: 'mqttjs_' + Math.random().toString(16).substr(2, 8),
  username: auth[0],
  password: auth[1],
};

/* Création d'une connection client */
var client = mqtt.connect(url, options);

/* Lorsque le client se connecte au cloud mqtt */
client.on('connect', function() { // When connected
  /* Il s'inscrit à un topic */
  client.subscribe('garden/temperature', function() {
    /* On récupère le message */
    client.on('message', function(topic, message, packet) {
      var string = message.toString();
      if (string.includes('temperature') == true){
        var jsObject = JSON.parse(message);
        webSocket.emit('temperature', jsObject.temperature.toString());
      } 
    });
  });

  client.subscribe('garden/airPressure', function() {
    /* On récupère le message */
    client.on('message', function(topic, message, packet) {
    var string = message.toString();
      if (string.includes('airPressure') == true){
        var jsObject = JSON.parse(message);
          webSocket.emit('pression', jsObject.airPressure.toString());
      }
    });
  }); 

  client.subscribe('garden/humidity', function() {
    /* On récupère le message */
    client.on('message', function(topic, message, packet) {
      /*On transforme le message ne String pour voir ce qu'il contient*/
    var string = message.toString();
    /* Si le message contient le mot humidity(clé), alors on désérialise le json 'message' 
    et on récupère la valeur de la clé 'humidity'*/
      if (string.includes('humidity') == true){
        var jsObject = JSON.parse(message);
          webSocket.emit('humidity', jsObject.humidity.toString());
      }
    });
  });

  client.subscribe('garden/accelerometer', function(){
    client.on('message', function(topic, message, packet){
      /* On transforme le message json en string pour voir s'il contient les clés que l'on desire*/
      var string = message.toString();

      /* Si le message (json) contient les mots (clés) que l'on veut : axes X, axes Y, axes Z alors:*/
      if (string.includes('axes X') == true && string.includes('axes Y') == true && string.includes('axes Z') == true){
        /* On transforme le résultat en chaine de caractères et on remplace les clés par des clés sans espaces*/
        var newString0 = string.replace('axes X', 'x');
        var newString1 = newString0.replace('axes Y', 'y');
        var finalString = newString1.replace('axes Z', 'z');

        /* On retransforme le résultat de la nouvelle chaine obtenue en json, qu'on renvoie sur la websocket au client */
        var messageJson = JSON.stringify(finalString);
        webSocket.emit('accelerometer', finalString);
      }
    });
  }); 
});
/***************************************************************************************************/ 