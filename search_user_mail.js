user_mail = "try.new.shai@gmail.com"
user_token = "1/oYVRk7YiY_nWRD0LlOnfjNEVvKDVGLQ2moPxqaqKewQ"
user_pwd = "m-sGj5UcLcN5Zb0m-xdbGXKb"
app_token = 'anonymous'
app_pwd = 'anonymous'


var sys = require('sys')
var exec = require('child_process').exec;

exports.search_mail = function (callback) {
  exec('python ./search_user_mail.py'+' '+app_token+' '+app_pwd+' '+user_mail+' '+user_token+' '+user_pwd, function (err, stdout, stderr) {
    if (err) return callback(err);
    callback(null, stdout);
  });
};

this.search_mail(function(err,res){
    if (err) {
    	console.log("errororor " + err);
    	return;
    }	
    console.log("alles gut :" + res);

});
