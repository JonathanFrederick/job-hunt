var httpRequest

function changeStatus(id_num) {
  httpRequest = new XMLHttpRequest();
  var st = document.getElementById(id_num).value;
  httpRequest.onreadystatechange = function() {
    if (alertContents() == true) {
      alert(httpRequest.responseText)
      moveNode(st, id_num)
    }
  };
  httpRequest.open('POST', '/update-status', true);
  httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  httpRequest.send("id_num="+id_num+"&status="+st);
};

function alertContents() {
  if (httpRequest.readyState == 4) {
    if (httpRequest.status === 200) {
      return true
    } else {
      alert('There was a problem with the request.');
      return false
    }
  }
};

function moveNode(new_st, id_num) {
  var old_node = document.getElementById(id_num).parentNode
  if (new_st == "NEVER") {
    old_node.parentNode.removeChild(old_node)
  }
  else {
    var new_par = document.getElementById(new_st)
    new_par.appendChild(old_node)
  }
}
