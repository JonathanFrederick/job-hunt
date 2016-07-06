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
  // get <li> to move
  var old_node = document.getElementById(id_num).parentNode
  if (new_st == "NEVER" || new_st == "REJECTED") {
    old_node.parentNode.removeChild(old_node)
  }
  else {
    // get new parent and existing <select> node
    var new_par = document.getElementById(new_st)
    var sel = old_node.getElementsByTagName("select")[0];
    // remove each existing <option> in the <select>
    var num_opts = sel.children.length;
    var i;
    for (i = 0; i<num_opts; i++) {
        sel.removeChild(sel.firstChild);
    }
    // get new <options>
    getOptions(id_num, new_st)
    // insert <li> into new <ul>
    if (httpRequest.responseText != false) {
      new_par.insertBefore(old_node, document.getElementById(httpRequest.responseText));
    } else {
      new_par.appendChild(old_node);
    };
  };
};

function getOptions(sel_id, status) {
  var sel = document.getElementById(sel_id);
  switch(status) {
    case "NEW":
      new_opts = ["NEVER", "LATER", "INTERESTED"];
      break;
    case "INTERESTED":
      new_opts = ["NEVER", "LATER", "APPLIED"];
      break;
    case "APPLIED":
      new_opts = ["REJECTED", "INTERVIEW"];
      break;
    case "INTERVIEW":
      new_opts = ["REJECTED", "OFFER"];
      break;
    case "OFFER":
      new_opts = ["ACCEPT?"];
      break;
    case "LATER":
      new_opts = ["NEVER", "INTERESTED"];
      break;
  }

  for (x in new_opts) {
    var new_opt = document.createElement("option");
    new_opt.value = new_opts[x];
    new_opt.selected = "selected";
    new_opt.appendChild(document.createTextNode(new_opts[x]))
    sel.insertBefore(new_opt, sel.firstChild)
  };
}
