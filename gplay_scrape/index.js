// GNU AGPL v3 or Later
// Written by John Nunley

const gplay = require('google-play-scraper');
const fs = require('fs');

function min(a, b) {
    return a < b ? a : b;
}

/**
 * Downloads app details from the Google Play store
 * @param{number} count - The number of apps to download
 * @returns{Promise} - A promise that resolves to an array of app details
 */
async function getApps(count) {
    const totalApps = [];
    while (totalApps.length < count) {
        const apps = await gplay.list({
            collection: gplay.collection.TOP_FREE,
            num: min(count, 500),
        });

        totalApps.push(...apps);
    }
    return totalApps;
}

function writeFile(path, data) {
    return new Promise((resolve, reject) => {
        fs.writeFile(path, data, (err) => {
            if (err) {
                reject(err);
            } else {
                resolve();
            }
        });
    });
}

async function main() {
    const count = parseInt(process.argv[2]);
    if (isNaN(count)) {
        console.error('Invalid count');
        process.exit(1);
    }

    const outFile = process.argv[3];
    if (!outFile) {
        console.error('Invalid output file');
        process.exit(1);
    }

    const apps = await getApps(500);
    await writeFile(outFile, JSON.stringify(apps));
}

main();

