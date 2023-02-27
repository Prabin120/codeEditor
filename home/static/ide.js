
// code editor
let editor;

window.onload = function () {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    // editor.setTheme("ace/theme/xcode");
    editor.session.setMode("ace/mode/c_cpp");
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true
    });
    editor.setFontSize(16);
}

let defaultMessage = "/*\n            Welcome to codeEditor \n     CTRL+ALT+ + : to increase the code editor size \n     CTRL+ALT+ -: to increase the code editor size \n   For more shortcur visit Shortcuts from setting icon*/\n\n\n"

$("#editor").text(defaultMessage)



function changeLanguage() {
    let language = $("#languages").val();

    if (language == "c" || language == "cpp") {
        editor.session.setMode("ace/mode/c_cpp");
        // $("#editor").text(defaultMessage+'#include<stdio.h>\nint main(){\n\tprintf("Hello codeEditor");\nreturn 0;\n}')
    }
    else if (language == "py") {
        editor.session.setMode("ace/mode/python");
        // $("#editor").text(defaultMessage+'print("Hello codeEditor")')
    }
    else if (language == "java") {
        editor.session.setMode("ace/mode/java");
        // $("#editor").text(defaultMessage+'class codeEditor{\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Hello, World!");\n\t}\n}')
    }
    else if (language == "js") {
        editor.session.setMode("ace/mode/javascript");
        // $("#editor").text(defaultMessage+'console.log("Hello codeEditor")')
    }
}

function executeCode() {
    $("#loading1").addClass("loading-overlay");
    $("#loading2").addClass("loading-spinner");
    $.ajax({
        url: "code/",
        method: "POST",
        data: {
            language: $("#languages").val(),
            code: editor.getSession().getValue(),
            input: $("#input").val()
        },
        success: function (response) {
            console.log(response);
            var output = response["output"];
            var error = response["error"];
            $("#loading1").removeClass("loading-overlay");
            $("#loading2").removeClass("loading-spinner");

            if (error != "") {
                error = error.replace(/\n/g, '<br>');
                $(".output").html(error);
            }
            else {
                output = output.replace(/\n/g, '<br>');
                $(".output").html(output);
            }
        }
    })
}

// Sortcuts for code editor
document.addEventListener("keydown", function (event) {
    if (event.ctrlKey && event.keyCode === 13) {
        // Get the current editor instance
        var editor = ace.edit("editor");

        // Move the cursor to the end of the current line
        editor.navigateLineEnd();

        // Insert a new line at the end of the current line
        editor.insert("\n");
    }
});



// Saving file
function saveFile() {
    let fileText = editor.getSession().getValue();
    let language = $("#languages").val();
    let blob = new Blob([fileText], { type: 'text/plain' });
    let fileName = 'codeEditor.' + language;
    let a = document.createElement('a');
    a.style.display = 'none';
    a.href = URL.createObjectURL(blob);
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}


// Event Listener

// Editor text size
var increaseButton = document.getElementById("increase-font-size");
var decreaseButton = document.getElementById("decrease-font-size");

// keyword listener
document.addEventListener("keydown", function (event) {
    if (event.ctrlKey && event.altKey && (event.key === "s" || event.key === "S")) {
        alert("You are pressing the save file")
        saveFile();
    }
    if (event.ctrlKey && event.altKey && (event.key === "+" || event.key === "=")) {
        var fontSize = editor.getFontSize();
        editor.setFontSize(fontSize + 2);
    }
    if (event.ctrlKey && event.altKey && (event.key === "_" || event.key === "-")) {
        var fontSize = editor.getFontSize();
        editor.setFontSize(fontSize - 2);
    }
    if (event.ctrlKey && event.altKey && event.keyCode == 13) {
        executeCode();
    }

})

function themeChange() {
    let theme = $("#theme").val();
    // console.log("Theme:" +theme)
    if (theme == "dark") {
        $("#theme").val("light");
        $("#theme").html("Dark Mode");
        editor.setTheme("ace/theme/xcode");
        $(".btn").addClass("light")
        $(".btn").css("color", "#272822")
        $("body").css("background-color", "#ECF2FF")
        $(".header").css("background-color", "#E3DFFD")
        $(".header").css("color", "rgb(52 135 133)")
        $("#input").css("background-color", "whitesmoke")
        $("#output").css("background-color", "whitesmoke")
        $("#input").css("color", "#272822")
        $("#output").css("color", "#272822")
        $(".row h5").css("color", "#272822")
    }
    else {
        $("#theme").val("dark");
        $("#theme").html("Light Mode");
        editor.setTheme("ace/theme/monokai")
        $(".btn").removeClass("light")
        $("body").css("background-color", "#2D2A46")
        $(".header").css("background-color", "#3D3B58")
        $(".header").css("color", "rgba(255, 255, 255, 0.7)")
        $("#input").css("background-color", "#272822")
        $("#output").css("background-color", "#272822")
        $("#input").css("color", "whitesmoke")
        $("#output").css("color", "whitesmoke")
        $(".row h5").css("color", "whitesmoke")
    }
}


// Get the modals and their close buttons
const shortcutsModal = document.getElementById("shortcuts-modal");
const feedbackModal = document.getElementById("feedback-modal");
const aboutModal = document.getElementById("about-modal");
const closeButtons = document.getElementsByClassName("close");

// Define a function to open a modal
function openModal(modal) {
  modal.style.display = "block";
}

// Define a function to close a modal
function closeModal(modal) {
  modal.style.display = "none";
}

// Attach click event listeners to the buttons
document.getElementById("shortcuts").addEventListener("click", function() {
  openModal(shortcutsModal);
});

document.getElementById("feedback").addEventListener("click", function() {
  openModal(feedbackModal);
});

document.getElementById("about").addEventListener("click", function() {
  openModal(aboutModal);
});

// Attach click event listeners to the close buttons
for (let i = 0; i < closeButtons.length; i++) {
  closeButtons[i].addEventListener("click", function() {
    const modal = this.parentElement.parentElement.parentElement;
    closeModal(modal);
  });
}

// Attach click event listener to the window to close the modal when clicked outside of it
window.addEventListener("click", function(event) {
  if (event.target == shortcutsModal) {
    closeModal(shortcutsModal);
  } else if (event.target == feedbackModal) {
    closeModal(feedbackModal);
  } else if (event.target == aboutModal) {
    closeModal(aboutModal);
  }
});

function feedback(){
    $("#loading1").addClass("loading-overlay");
    $("#loading2").addClass("loading-spinner");
    $.ajax({
        url: "feedback/",
        method: "POST",
        data: {
            name:$("#name").val(),
            email:$("#email").val(),
            message:$("#message").val()
        },
        success: function (response) {
            $("#loading1").removeClass("loading-overlay");
            $("#loading2").removeClass("loading-spinner");
            $("#feedback-message").html("Thank You for your feedback.")
        }
    })
}