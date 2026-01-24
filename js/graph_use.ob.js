var _$_9348=["","top","center","bold","calibri","dimGrey","line","Float","Chart","render"];

function drawgraph(_0x95EF,_0x95BF,_0x961F,_0x964F){
    // Calculate linear fit
    var n = _0x95BF.length;
    var sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
    for(var i=0; i<n; i++) {
        sumX += _0x95BF[i].x;
        sumY += _0x95BF[i].y;
        sumXY += _0x95BF[i].x * _0x95BF[i].y;
        sumX2 += _0x95BF[i].x * _0x95BF[i].x;
    }
    var slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    var intercept = (sumY - slope * sumX) / n;

    // Create fit points
    var fitPoints = [];
    if (n > 1) {
        var minX = _0x95BF[0].x;
        var maxX = _0x95BF[n-1].x;
        fitPoints.push({x: minX, y: slope * minX + intercept});
        fitPoints.push({x: maxX, y: slope * maxX + intercept});
    }

    var _0x958F= new CanvasJS[_$_9348[8]](_0x95EF,{
        zoomEnabled:true,
        title:{text:_$_9348[0]},
        toolTip:{shared:false},
        legend:{verticalAlign:_$_9348[1],horizontalAlign:_$_9348[2],fontSize:14,fontWeight:_$_9348[3],fontFamily:_$_9348[4],fontColor:_$_9348[5]},
        axisX:{title:_0x961F},
        axisY:{title:_0x964F,includeZero:false},
        data:[
            {
                type: "scatter",
                xValueType:_$_9348[7],
                showInLegend:false,
                name: "Observations",
                markerSize: 10,
                dataPoints:_0x95BF
            },
            {
                type: "line",
                showInLegend: true,
                name: "Linear Fit (Slope: " + slope.toExponential(3) + ")",
                markerSize: 0,
                dataPoints: fitPoints
            }
        ]
    });
    _0x958F[_$_9348[9]]();
}
