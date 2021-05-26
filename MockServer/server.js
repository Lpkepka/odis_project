const express = require('express')
const app = express()
const port = 3010

app.get('/', (req, res) => {
  res.send('Hello World')
})

app.get("/api", function(req, res)  { 
        var fs = require('fs');
        fs.readFile('log.txt', 'utf8', function(err,data) {
            if(err) throw err;
            let splitted = data.toString().split("\n");
            var json = { "Logs" : splitted };
            res.json(json)
        });
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})