document.addEventListener("DOMContentLoaded", function () {
    function getCsrfToken() {

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        return csrfToken;
    }

    function sendUpdate(param, value) {
        fetch(`/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({ [param]: value }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
        });
    }

    function saveDrawing() {
        let canvas = document.querySelector("canvas")[1];
        console.log(canvas)

        if (!canvas) {
            console.error("Canvas not found");
            return;
        }

        let imageData = canvas.toDataURL("image/png");
        console.log(canvas.toDataURL("image/png"));

        fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({ image: imageData }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("Drawing saved successfully at C:\\Users\\user\\Documents\\Artline Pictures");
            } else {
                alert("Error saving drawing: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }

    function clearCanvas() {
        fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({ clear_canvas: true }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("Canvas cleared!");
            } else {
                alert("Error clearing canvas: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }

    // Size Buttons
    document.getElementById("big-size").addEventListener("click", function () {
        sendUpdate("thickness", 10);
    });
    document.getElementById("medium-size").addEventListener("click", function () {
        sendUpdate("thickness", 5);
    });
    document.getElementById("small-size").addEventListener("click", function () {
        sendUpdate("thickness", 2);
    });

    // Color Buttons
    document.getElementById("black-btn").addEventListener("click", function () {
        sendUpdate("color_index", 0);
        sendUpdate("eraser_mode", false);
    });
    document.getElementById("red-btn").addEventListener("click", function () {
        sendUpdate("color_index", 1);
        sendUpdate("eraser_mode", false);
    });
    document.getElementById("green-btn").addEventListener("click", function () {
        sendUpdate("color_index", 2);
        sendUpdate("eraser_mode", false);
    });
    document.getElementById("blue-btn").addEventListener("click", function () {
        sendUpdate("color_index", 3);
        sendUpdate("eraser_mode", false);
    });
    document.getElementById("yellow-btn").addEventListener("click", function () {
        sendUpdate("color_index", 4);
        sendUpdate("eraser_mode", false);
    });
    document.getElementById("purple-btn").addEventListener("click", function () {
        sendUpdate("color_index", 5);
        sendUpdate("eraser_mode", false);
    });

    // Eraser Button
    document.getElementById("eraser-tab").addEventListener("click", function () {
        sendUpdate("eraser_mode", true);
    });

    document.getElementById("save-tab").addEventListener("click", function () {
        saveDrawing();
    });

    document.getElementById("delete-popup").addEventListener("click", clearCanvas);
});
