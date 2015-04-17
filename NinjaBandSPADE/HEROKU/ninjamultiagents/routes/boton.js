
/*
 * GET home page.
 */

exports.boton = function(req, res){
  res.render('index', { title: 'Ninjafying your home' });
   // res.send("No puedo encontrar la pagina que el Dr. Brena busca");
};