const fs = require('fs');
const path = require('path');

function validateJson(filePath) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    const parsed = JSON.parse(data);
    console.log(`✅ ${path.basename(filePath)} is valid JSON! Contains ${parsed.length} entries.`);
    return true;
  } catch (e) {
    console.error(`❌ Error parsing ${path.basename(filePath)}:`, e.message);
    return false;
  }
}

const categoriesPath = path.join(__dirname, '../data/categories.json');
const promptsPath = path.join(__dirname, '../data/prompts.json');

const catValid = validateJson(categoriesPath);
const promptsValid = validateJson(promptsPath);

if (catValid && promptsValid) {
  console.log("All data files validated successfully!");
  process.exit(0);
} else {
  console.error("Data validation failed!");
  process.exit(1);
}
