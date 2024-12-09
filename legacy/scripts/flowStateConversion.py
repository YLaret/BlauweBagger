// Load payload
// var data = msg.payload[8];
// msg.payload = data

// Load EM states
var f200qa = {payload: (msg.payload[0]/4095*16*12.1875), topic: "DV1"};
var f250qa = {payload: (msg.payload[1]/4095*16*14.84375), topic: "DV1"};
var f25ad = {payload: (msg.payload[2]/4095*16*8.8125), topic: "DV1"};

return [f200qa,f250qa,f25ad];



return msg;
