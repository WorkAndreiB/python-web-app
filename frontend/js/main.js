const generateButton = document.getElementById("generate-button");
const copyButton = document.getElementById("copy-button");
const passwordLengthInput = document.getElementById("password-length");
const passwordOutput = document.getElementById("generated-password");

copyButton.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(passwordOutput.textContent ?? "");
        copyButton.textContent = "Copied!";
    } catch (error) {
        copyButton.textContent = "Copy failed";
        console.error("Failed to copy password to clipboard.", error);
    }
});

generateButton.addEventListener("click", async () => {
    const length = passwordLengthInput.value;

    passwordOutput.textContent = "Generating...";
    copyButton.textContent = "Copy Password";

    try {
        const response = await fetch(
            `http://localhost:8000/password/generate-pass?length=${length}`
        );

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();

        passwordOutput.textContent = data.password;

    } catch (error) {
        passwordOutput.textContent = "Failed to generate password.";
        console.error(error);
    }
});