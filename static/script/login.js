function switchForm(form) {
        let loginForm = document.getElementById("loginForm");
        let signupForm = document.getElementById("signupForm");

        if (form === "signup") {
            loginForm.style.display = "none";
            signupForm.style.display = "block";
        } else {
            signupForm.style.display = "none";
            loginForm.style.display = "block";
        }
    }