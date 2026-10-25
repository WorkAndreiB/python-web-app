import { generatePassword } from "./api.js";

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
    const length = Number(passwordLengthInput.value);

    if (!Number.isInteger(length) || length < 8 || length > 128) {
        passwordOutput.textContent =
            "Password length must be between 8 and 128.";
        return;
    }
    passwordOutput.textContent =
            "Password length must be between 8 and 128.";
    passwordOutput.textContent = "Generating...";
    copyButton.disabled = true;
    copyButtonLabel.textContent = "Copy";

    try {
        const password = await generatePassword(length);

        passwordOutput.textContent = password;
        copyButton.disabled = false;

    } catch (error) {
        passwordOutput.textContent = "Failed to generate password.";
        console.error(error);
    }
});