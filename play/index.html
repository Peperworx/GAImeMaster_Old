<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title>gAImeMaster</title>
    <style>
        html, body {
            width:100%;
            height:100%;
            margin:0;
        }
        .dialog {
            height:50%;
            width:auto;
        }
        .diaimg {
            height:100%;
            width:auto;
        }
        p {}
        .clssReq {
            display:none;
        }
        #charactersheet {
            padding:1%;
        }
    </style>
    <script src="/static/socket.io.js"></script>
    <script src="/static/jquery.js"></script>
</head>
<body>
    <div id="charactersheet">
        <div class="clssReq">&nbsp;Hit Points:<span id="hp"></span></div>
        <div class="clssReq">&nbsp;Armor Class:<span id="ac"></span></div>
        <h3>&nbsp;Ability Scores:</h3>
        <pre>&nbsp;&nbsp;Strength:     <span id="str"></span></pre>
        <pre>&nbsp;&nbsp;Intelligence: <span id="int"></span></pre>
        <pre>&nbsp;&nbsp;Wisdom:       <span id="wis"></span></pre>
        <pre>&nbsp;&nbsp;Dexterity:    <span id="dex"></span></pre>
        <pre>&nbsp;&nbsp;Constitution: <span id="con"></span></pre>
        <pre>&nbsp;&nbsp;Charisma:     <span id="cha"></span></pre>
        <button class="noClssReq" id="selectClss">Continue</button>
        <div class="clssReq">
            <h3>&nbsp;Saving Throws:</h3>
            <pre>&nbsp;&nbsp;Poison or Death Ray: <span id="PDR">Please type in class and press finish.</span></pre>
            <pre>&nbsp;&nbsp;Magic Wand: <span id="MW">Please type in class and press finish.</span></pre>
            <pre>&nbsp;&nbsp;Turn to Stone or Paralysis: <span id="TTSP">Please type in class and press finish.</span></pre>
            <pre>&nbsp;&nbsp;Dragon Breath: <span id="DB">Please type in class and press finish.</span></pre>
            <pre>&nbsp;&nbsp;Spells or Magic Staff: <span id="SMS">Please type in class and press finish.</span></pre>
        </div>
        <button class="clssReq" id="save">Save</button>
    </div>
</body>
<script>
    var socket = io("localhost:3545/");
    socket.emit("generate", "");
    var uc
    socket.on("generated", function (msg) {
        var msg = JSON.parse(msg);
        $("#lvl").text(msg["level"]);
        $("#str").text(msg["stats"]["str"]);
        $("#int").text(msg["stats"]["int"]);
        $("#wis").text(msg["stats"]["wis"]);
        $("#dex").text(msg["stats"]["dex"]);
        $("#con").text(msg["stats"]["con"]);
        $("#cha").text(msg["stats"]["cha"]);
        uc = msg
        
    });
    $("#selectClss").click(function (event) {
        var characterName = window.prompt("Please enter charactername here:");
        var characterClss = window.prompt("Please enter characters class here:");
        var characterAlign = window.prompt("Please enter characters alignment here:");
        socket.emit("cplt", JSON.stringify([characterName, characterClss, characterAlign, uc]))

    });
    socket.on("finish", function (msg) {
        msg = JSON.parse(msg)
        $("#lvl").text(msg["level"]);
        $("#str").text(msg["stats"]["str"]);
        $("#int").text(msg["stats"]["int"]);
        $("#wis").text(msg["stats"]["wis"]);
        $("#dex").text(msg["stats"]["dex"]);
        $("#con").text(msg["stats"]["con"]);
        $("#cha").text(msg["stats"]["cha"]);
        $("#cha").text(msg["stats"]["cha"]);
        $("#PDR").text(msg["savingThrows"][0]);
        $("#MW").text(msg["savingThrows"][1]);
        $("#TTSP").text(msg["savingThrows"][2]);
        $("#DB").text(msg["savingThrows"][3]);
        $("#SMS").text(msg["savingThrows"][4]);
        $("#hp").text(msg["hp"]);
        $("#ac").text(msg["armorClass"]);
        $(".clssReq").show();
        $(".noClssReq").hide();
        console.log("finish");
        uc = msg
    });
    $("#save").click(function (event) {
        socket.emit("save", JSON.stringify(uc));
    });
    socket.on("saved", function (msg) {
        msg = JSON.parse(msg);
        alert("Character saved! ID is: "+msg["id"]+". Save this so you can load your character next time you play.");
    });
</script>
</html>
