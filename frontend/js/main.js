const generateButton = document.getElementById("generate-button");
const copyButton = document.getElementById("copy-button");
const copyButtonLabel = copyButton.querySelector("span");
const passwordLengthInput = document.getElementById("password-length");
const passwordOutput = document.getElementById("generated-password");

copyButton.disabled = true;

copyButton.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(passwordOutput.textContent ?? "");
        copyButtonLabel.textContent = "Copied!";
    } catch (error) {
        copyButtonLabel.textContent = "Copy failed";
        console.error("Failed to copy password to clipboard.", error);
    }
});

generateButton.addEventListener("click", async () => {
    const length = passwordLengthInput.value;

    passwordOutput.textContent = "Generating...";
    copyButton.disabled = true;
    copyButtonLabel.textContent = "Copy";

    try {
        const response = await fetch(
            `http://localhost:8000/password/generate-pass?length=${length}`
        );

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();

        passwordOutput.textContent = data.password;
        copyButton.disabled = false;

    } catch (error) {
        passwordOutput.textContent = "Failed to generate password.";
        console.error(error);
    }
});