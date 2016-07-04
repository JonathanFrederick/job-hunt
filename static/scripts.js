var httpRequest

function changeStatus(id_num) {
  httpRequest = new XMLHttpRequest();
  var st = document.getElementById(id_num).value;
  httpRequest.onreadystatechange = function() {
    if (alertContents() == true) {
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
    switch(new_st) {
      case "INTERESTED":
        next_st = ["APPLIED"]
        break;
      case "APPLIED":
        next_st = ["REJECTED", "INTERVIEWED"]
        break;
      case "INTERVIEWED":
        next_st = ["OFFER"]
        break;
      case "MAYBE LATER":
        next_st = ["INTERESTED"]
        break;
    };
    var sel = old_node.getElementsByTagName("select")[0];
    sel.removeChild(sel.querySelectorAll("[value="+new_st+"]")[0]);
    for (x in next_st) {
      var new_opt = document.createElement("option");
      new_opt.value = next_st[x];
      new_opt.selected = "selected";
      new_opt.appendChild(document.createTextNode(next_st[x]))
      sel.insertBefore(new_opt, sel.firstChild)
    };
    if (httpRequest.responseText != false) {
      new_par.insertBefore(old_node, document.getElementById(httpRequest.responseText));
    } else {
      new_par.appendChild(old_node);
    };
  };
};
