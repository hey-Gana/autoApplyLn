const express = require('express');
const path = require('path');
const fs = require('fs'); // for writing files
const multer = require('multer'); // for handling file uploads
const { spawn } = require("child_process"); //running script in the background terminal

const app = express();
const host = '127.0.0.1';
const port = 3000;

// Set up EJS for rendering HTML templates
app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// Ensure 'uploads' directory exists
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
}

// Set up multer storage configuration
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, __dirname); // Save files within the directory
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname); // Use original filename
    }
});
const upload = multer({ storage: storage });

// Serve the form page
app.get('/', (req, res) => {
    res.render("form", { submitted: false, formData: null });
});

// Route for handling form submission (Creates `config.py`)
app.post("/save-config", upload.single('resume'), (req, res) => {
    const config = req.body; // Form data

    // Ensure default value for 'head' if not set
    const headValue = config.head === "yes" ? "True" : "False";
    const resumeFile = req.file ? req.file.filename : "No file uploaded";

    // Convert form data into Python config format
    const pyConfig = `
# Config file generated from form submission
fname = "${config.fname}"
lname = "${config.lname}"
phno = "${config.phno}"
city = "${config.city}"
email = "${config.email}"
pw = "${config.pw}"
role = "${config.role}"
loc = "${config.loc}"
yoe = "${config.yoe}"
resume = "${resumeFile}"
head = ${headValue}`;

    const configFilePath = path.join(__dirname, 'config.py');
    console.log('Writing config to:', configFilePath);

    // Write the config to a file
    fs.writeFile(configFilePath, pyConfig, (err) => {
        if (err) {
            console.error('Error writing the config file:', err);
            return res.status(500).send('Error writing the config file');
        }

        // Render the page with submitted data
        res.render("form", {
            submitted: true,
            formData: { ...config, resume: resumeFile }
        });
    });
});

// Route to handle automation script execution
app.post("/run-script", (req, res) => {
    console.log("Running command: python3 auto.py"); // Log of command being executed
//    exec("python3 auto.py ", (error, stdout, stderr) => { //runs python in the background
//        if (error) {
//            console.error(`Error executing script: ${error.message}`);
//            return res.send("Error running the script.");
//        }
//        console.log(`Script output: ${stdout}`);
//    });
    const process = spawn("python3", ["auto.py"], { stdio: "inherit" });
    res.send("Script execution started successfully! Please check your terminal.You can close this browser now.");
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://${host}:${port}`);
});
