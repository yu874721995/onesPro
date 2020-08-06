var port = 'https://yushifamily.club';
var testPort = 'http://192.168.10.127:9001';
function getport(rl) {
    if(rl=='test'){
        return testPort;
    }else if(rl=='master'){
        return port;
    };
};

hostUrl = getport('test')
