import React from 'react';

class CSRFToken extends React.Component {
	constructor(props) {
	  super(props);
	}

	getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log("COOKIE VALUE:")
    console.log(cookieValue)
    return cookieValue;
	}

	render() {
		var csrfCookie = this.getCookie('csrftoken')
    return (
        <input type="hidden" name="csrfmiddlewaretoken" value={csrfCookie} />
    )
  }
}
export default CSRFToken;