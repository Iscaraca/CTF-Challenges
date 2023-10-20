const EmscriptenModule = require('./site.js');

async function initializeModule() {
    return new Promise((resolve, reject) => {
        EmscriptenModule.onRuntimeInitialized = () => {
            const CraftQuery = EmscriptenModule.cwrap('craft_query', 'string', ['string', 'string']);
            resolve(CraftQuery);
        };
    });
}

let CraftQuery;
initializeModule().then((queryFunction) => {
    CraftQuery = queryFunction;
});

exports.handler = async (event, context) => {
    if (!CraftQuery) {
        CraftQuery = await initializeModule();
    }

    const username = event.username;
    const password = event.password;

    const result = CraftQuery(username, password);
    return result;
};