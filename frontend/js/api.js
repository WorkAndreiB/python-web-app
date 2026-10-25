const API_BASE_URL = "http://localhost:8000";

// export makes the function available for import in other js files
// async indicates that the function returns a promise and can be awaited
export async function generatePassword(length) {
    const response = await fetch(
        `${API_BASE_URL}/password/generate-pass?length=${length}`
    );

    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();

    return data.password;
}