// Refer to https://stackoverflow.com/questions/40172921/how-to-add-new-column-to-csv-file-using-node-js
var csv = require('csv-parser');
var fs = require('fs');
var json2csv = require('json2csv');
var dataArray = [];

fs.createReadStream('your-original-csv-file.csv')
  .pipe(csv())
  .on('data', function (data) {
    data.newColumn = newColumnValue;
    dataArray.push(data);
  })
  .on('end', function(){
    var result = json2csv({ data: dataArray, fields: Object.keys(dataArray[0]) });
    fs.writeFileSync(fileName, result);
  });