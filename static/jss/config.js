var port = 'https://yushifamily.club';
var testPort = 'http://121.201.57.207:9001';
function getport(rl) {
    if(rl=='test'){
        return testPort;
    }else if(rl=='master'){
        return port;
    };
};

hostUrl = getport('test')
