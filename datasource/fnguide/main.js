const puppeteer = require('puppeteer');
const axios = require('axios');
const fs = require('fs');

const sayHello = () => {
    const url = 'http://api.simpli.kr/tickers/?token=blendedrequesttoken';
    axios.get(url)
         .then((res) => {
            console.log(JSON.stringify(res.data));
         })
         .catch((err) => {
            throw err;
         });
};

sayHello();