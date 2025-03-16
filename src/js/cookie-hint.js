
function setCookie(cname, cvalue, exdays) {
  /* https://www.w3schools.com/js/js_cookies.asp */
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = 'expires='+d.toUTCString();
  document.cookie = cname + '=' + cvalue + ';' + expires + ';path=/';
}

function getCookie(cname) {
  /* https://www.w3schools.com/js/js_cookies.asp */
  var name = cname + '=';
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return '';
}

function cookieHint(termsLink) {
  var host = window.location.host.toLowerCase();
  var accepted = getCookie('cookiesAccepted').toLowerCase();
  if(accepted != host) {
    var hintDiv = document.createElement('div');
    hintDiv.id = 'cookie-hint';
    hintDiv.className = 'cookie-hint';
    var hintInner = document.createElement('div');
    hintDiv.appendChild(hintInner)
    hintInner.appendChild(document.createTextNode('This website uses cookies. '));
    var hintLink = document.createElement('a');
    hintLink.setAttribute('href', termsLink);
    hintLink.appendChild(document.createTextNode('Read More'));
    hintInner.appendChild(hintLink);
    hintInner.appendChild(document.createTextNode('. '));
    var hintButton = document.createElement('button');
    hintButton.setAttribute('type', 'button');
    hintButton.addEventListener(
      'click',
      function (e) {
        var hintDiv = document.getElementById('cookie-hint');
        if (hintDiv !== null) {
          hintDiv.style.visibility = 'hidden';
          setCookie('cookiesAccepted', host, 365);
        }
      },
      false);
    hintButton.appendChild(document.createTextNode('Got It!'));
    hintInner.appendChild(hintButton);
    document.body.appendChild(hintDiv);
  }
}
