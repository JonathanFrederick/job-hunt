var httpRequest

function changeStatus(id_num) {
  httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = alertContents
  httpRequest.open('POST', '/update-status', true);
  httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  httpRequest.send("id_num="+id_num+"&status="+document.getElementById(id_num).value);
};

function alertContents() {
  if (httpRequest.readyState == 4) {
    if (httpRequest.status === 200) {
      alert(httpRequest.responseText);
    } else {
      alert('There was a problem with the request.');
    }
  }
};
