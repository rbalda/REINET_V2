function inicializar(){
    addConsultant.addEventListener("click", nuevoCon, false);
    addJudge.addEventListener("click", nuevoJur, false);
    addScope.addEventListener("click", nuevoSco, false);
    addMilestone.addEventListener("click", nuevoMile, false);
}

function nuevoCon(){
    var nuevoC = document.createElement("input");
    //var idcont = consultat.childElementCount()-3;
    nuevoC.setAttribute("type", "text");
    nuevoC.setAttribute("class", "form-control");
    //nuevoC.setAttribute("id", "consultor"+idcont);
    nuevoC.setAttribute("placeholder", "Ingrese el nombre de un usuario para invitarlo como consultor");

    consultant.insertBefore(nuevoC, addConsultant);
}

function nuevoJur(){
    var nuevoJ = document.createElement("input");
    //var idcont = judge.childElementCount()-3;
    nuevoJ.setAttribute("type", "text");
    nuevoJ.setAttribute("class", "form-control");
    //nuevoC.setAttribute("id", "jurado"+idcont);
    nuevoJ.setAttribute("placeholder", "Ingrese el nombre de un usuario para invitarlo como jurado");

    judge.insertBefore(nuevoJ, addJudge);
}

function nuevoSco(){
    var nuevoS = document.createElement("select");
    var opc0 = document.createElement("option");
    var txtSel = document.createTextNode("Seleccione uno");
    var opc1 = document.createElement("option");
    var txtEspol = document.createTextNode("ESPOL");
    var opc2 = document.createElement("option");
    var txtUSM = document.createTextNode("USM");
    var opc3 = document.createElement("option");
    var txtUEES = document.createTextNode("UEES");

    nuevoS.setAttribute("class", "form-control");
    opc0.setAttribute("value", "");
    opc1.setAttribute("value", "ESPOL");
    opc2.setAttribute("value", "USM");
    opc3.setAttribute("value", "UEES");
    opc0.setAttribute("selected", "selected");

    opc0.appendChild(txtSel);
    opc1.appendChild(txtEspol);
    opc2.appendChild(txtUSM);
    opc3.appendChild(txtUEES);

    nuevoS.appendChild(opc0);
    nuevoS.appendChild(opc1);
    nuevoS.appendChild(opc2);
    nuevoS.appendChild(opc3);

    scope.insertBefore(nuevoS, addScope);
}

function nuevoMile(){
    var linea = document.createElement("hr");
    var divFe = document.createElement("div");
    var lblFe = document.createElement("label");
    var txtFe = document.createTextNode("Fecha de entrega");
    var inputFe = document.createElement("input");
    var divPe = document.createElement("div");
    var lblPe = document.createElement("label");
    var txtPe = document.createTextNode("Peso en porcentaje");
    var inputPe = document.createElement("input");

    divFe.setAttribute("class", "form-group");
    lblFe.setAttribute("for", "due-date");
    lblFe.appendChild(txtFe);
    inputFe.setAttribute("type", "date");
    inputFe.setAttribute("class", "form-control");
    divFe.appendChild(lblFe);
    divFe.appendChild(inputFe);

    divPe.setAttribute("class", "form-group");
    lblPe.setAttribute("for", "percent");
    lblPe.appendChild(txtPe);
    inputPe.setAttribute("type", "number");
    inputPe.setAttribute("class", "form-control");
    inputPe.setAttribute("min", "0");
    inputPe.setAttribute("max", "100");
    inputPe.setAttribute("step", "5");
    divPe.appendChild(lblPe);
    divPe.appendChild(inputPe);

    var contador = milestones.childElementCount;
    contador = (contador / 4)+1;

    var txtMile = document.createTextNode("Milestone " + contador);
    var subtitulo = document.createElement("h4");
    subtitulo.appendChild(txtMile);

    milestones.appendChild(subtitulo);
    milestones.appendChild(linea);
    milestones.appendChild(divFe);
    milestones.appendChild(divPe);
}

window.addEventListener("load", inicializar, false);