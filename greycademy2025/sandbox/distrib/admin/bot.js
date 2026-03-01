const puppeteer = require('puppeteer')
const net = require('net')

const BASE_URL = process.env.BASE_URL
const FLAG = process.env.FLAG

const browserPool = []
const waiting_jobs = []
const POOL_SIZE = Number(process.env.BROWSER_POOL_SIZE || 3)

const getBrowser = async () => {
    if (browserPool.length > 0) {
        return browserPool.pop()
    }

    return await new Promise((resolve) => {
        waiting_jobs.push(resolve)
    })
}

const returnBrowser = (browser) => {
    if (waiting_jobs.length > 0) {
        const do_job = waiting_jobs.shift()
        do_job(browser)
        return
    }
    browserPool.push(browser)
}

const visitSubmission = async (url) => {
    const browser = await getBrowser()
    const page = await browser.newPage()

    const base = new URL(process.env.BASE_URL);
    const u = new URL(url)
    u.protocol = base.protocol;
    u.hostname = base.hostname;
    u.port = base.port;

    await page.setCookie({
        name: 'session',
        value: FLAG,
        url: u.origin,
        path: '/',
        httpOnly: false,
        secure: false,
        sameSite: 'Lax'
    })
    try {
        await page.goto(u, { waitUntil: 'networkidle2', timeout: 5000 })
    }
    catch (e) {
        console.log(e)
    }
    await page.close()
    returnBrowser(browser)
}


const server = net.createServer((socket) => {
    socket.on('data', async (data) => {
        const id = data.toString().trim()
        await visitSubmission(id)
    })
})

const initPool = async () => {
    for (let i = 0; i < POOL_SIZE; i += 1) {
        const browser = await puppeteer.launch({
            headless: true,
            args: ['--js-flags=--jitless', '--no-sandbox', '--disable-setuid-sandbox']
        })
        returnBrowser(browser)
    }
}

initPool().then(() => {
    server.listen(3001, () => {
        console.log('Listening on port 3001')
    })
})
