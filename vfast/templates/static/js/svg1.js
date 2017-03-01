;( function() {
  var data = {
    lineChart : [
      {
        date  : '2016-09-22',
        label : '2016-09-22',
        value : 0
      },
      {
        date  : '2016-09-23',
        label : '2016-09-23',
        value : 2
      },
      {
        date  : '2016-09-24',
        label : '2016-09-24',
        value : 3
      },
      {
        date  : '2016-09-25',
        label : '2016-09-25',
        value : 3
      },
      {
        date  : '2016-09-26',
        label : '2016-09-26',
        value : 3
      },
      {
        date  : '2016-09-27',
        label : '2016-09-27',
        value : 2
      },
      {
        date  : '2016-09-28',
        label : '2016-09-28',
        value : 1
      }
    ]
  };
  
  var DURATION = 1000;

  /**
   * draw the fancy line chart
   *
   * @param {String} elementId elementId
   * @param {Array}  data      data
   */
  function drawLineChart( elementId, data ) {
    // parse helper functions on top
    var parse = d3.time.format( '%Y-%m-%d' ).parse;
    // data manipulation first
    data = data.map( function( datum ) {
      datum.date = parse( datum.date );
      return datum;
    } );

      //console.log( data );
    // TODO code duplication check how you can avoid that
    var containerEl = document.getElementById( elementId ),
        width       = 900,
        height      = 400,
        margin      = {
            top    : 50,
            right  : 10,
            left   : 10
        },

        detailWidth  = 98,
        detailHeight = 55,
        detailMargin = 10,

        container   = d3.select( containerEl ),
        svg         = container.select( 'svg' )
            .attr( 'width', width )
            .attr( 'height', height + margin.top ),

        x          = d3.time.scale().range( [ 0, width - detailWidth ] ),
        xAxis      = d3.svg.axis().scale( x )
                                  .ticks ( 8 )
                                  .tickSize( -height ),
        //xAxisTicks = d3.svg.axis().scale( x )
        //                          .ticks( 16 )
        //                          .tickSize( -height )
        //                          .tickFormat( '' ),
        y          = d3.scale.linear().range( [ height, 0 ] ),
        yAxisTicks = d3.svg.axis().scale( y )
                                  .ticks( 5 )
                                  .tickSize( width )
                                  .tickFormat( '' )
                                  .orient( 'right' ),
        
        area = d3.svg.area()
                      .interpolate( 'linear' )
                      .x( function( d )  { return x( d.date ) + detailWidth / 2; } )
                      .y0( height )
                      .y1( function( d ) { return y( d.value*100 ); } ),

        line = d3.svg.line()
                  .interpolate( 'linear' )
                  .x( function( d ) { return x( d.date ) + detailWidth / 2; } )
                  .y( function( d ) { return y( d.value*100 ); } ),
        
        startData = data.map( function( datum ) {
                      return {
                        date  : datum.date,
                        value : 0
                      };
                    } ),
        
        circleContainer;

    
    // Compute the minimum and maximum date, and the maximum price.
    x.domain( [ data[ 0 ].date, data[ data.length - 1 ].date ] );
    // hacky hacky hacky :(
    y.domain( [ 0, d3.max( data, function( d ) { return d.value*125; } )  ] );

    //svg.append( 'g' )
    //    .attr( 'class', 'lineChart--xAxisTicks' )
    //    .attr( 'transform', 'translate(' + detailWidth / 2 + ',' + height + ')' )
    //    .call( xAxisTicks );

    svg.append( 'g' )
        .attr( 'class', 'lineChart--xAxis' )
        .attr( 'transform', 'translate(' + detailWidth / 2 + ',' + ( height + 20 ) + ')' )
        .call( xAxis );
    
    svg.append( 'g' )
      .attr( 'class', 'lineChart--yAxisTicks' )
      .call( yAxisTicks );

    // Add the line path.
    svg.append( 'path' )
        .datum( startData )
        .attr( 'class', 'lineChart--areaLine' )
        .attr( 'd', line )
        .transition()
        .duration( DURATION )
        .delay( DURATION / 2 )
        .attrTween( 'd', tween( data, line ) )
        .each( 'end', function() {
          drawCircles( data );
        } );
    
    
    // Add the area path.
    svg.append( 'path' )
        .datum( startData )
        .attr( 'class', 'lineChart--area' )
        .attr( 'd', area )
        .transition()
        .duration( DURATION )
        .attrTween( 'd', tween( data, area ) );
    
    // Helper functions!!!
    function drawCircle( datum, index ) {
      circleContainer.datum( datum )
                    .append( 'circle' )
                    .attr( 'class', 'lineChart--circle' )
                    .attr( 'r', 0 )
                    .attr(
                      'cx',
                      function( d ) {
                        return x( d.date ) + detailWidth / 2;
                      }
                    )
                    .attr(
                      'cy',
                      function( d ) {
                        return y( d.value*100 );
                      }
                    )
                    .on( 'mouseenter', function( d ) {
                      d3.select( this )
                        .attr(
                          'class',
                          'lineChart--circle lineChart--circle__highlighted' 
                        )
                        .attr( 'r', 8 );
                      
                        d.active = true;
                        
                        showCircleDetail( d );
                    } )
                    .on( 'mouseout', function( d ) {
                      d3.select( this )
                        .attr(
                          'class',
                          'lineChart--circle' 
                        )
                        .attr( 'r', 7 );
                      
                      if ( d.active ) {
                        hideCircleDetails();
                        
                        d.active = false;
                      }
                    } )
                    .on( 'click touch', function( d ) {
                      if ( d.active ) {
                        showCircleDetail( d )
                      } else {
                        hideCircleDetails();
                      }
                    } )
                    .transition()
                    .delay( DURATION / 10 * index )
                    .attr( 'r', 7 );
    }
    
    function drawCircles( data ) {
      circleContainer = svg.append( 'g' );

      data.forEach( function( datum, index ) {
        drawCircle( datum, index );
      } );
    }
    
    function hideCircleDetails() {
      circleContainer.selectAll( '.lineChart--bubble' )
                      .remove();
    }
    
    function showCircleDetail( data ) {
      var details = circleContainer.append( 'g' )
                        .attr( 'class', 'lineChart--bubble' )
                        .attr(
                          'transform',
                          function() {
                            var result = 'translate(';
                            result += x( data.date );
                            result += ', ';
                            result += y( data.value*100 ) - detailHeight - detailMargin;
                            result += ')';
                            return result;
                          }
                        );

      details.append( 'path' )
              .attr( 'd', 'M2.99990186,0 C1.34310181,0 0,1.34216977 0,2.99898218 L0,47.6680579 C0,49.32435 1.34136094,50.6670401 3.00074875,50.6670401 L44.4095996,50.6670401 C48.9775098,54.3898926 44.4672607,50.6057129 49,54.46875 C53.4190918,50.6962891 49.0050244,54.4362793 53.501875,50.6670401 L94.9943116,50.6670401 C96.6543075,50.6670401 98,49.3248703 98,47.6680579 L98,2.99898218 C98,1.34269006 96.651936,0 95.0000981,0 L2.99990186,0 Z M2.99990186,0' )
              .attr( 'width', detailWidth )
              .attr( 'height', detailHeight )
          .attr('fill','#FFF');
      
      var text = details.append( 'text' )
                        .attr( 'class', 'lineChart--bubble--text' );

      text.append( 'tspan' )
          .attr( 'class', 'lineChart--bubble--label' )
          .attr( 'x', detailWidth / 2 )
          .attr( 'y', detailHeight / 3 )
          .attr( 'text-anchor', 'middle' )
          .attr( 'fill','white')
          .text( data.date.getFullYear()+"-"+(data.date.getMonth()+1)+"-"+data.date.getDate() );

      text.append( 'tspan' )
          .attr( 'class', 'lineChart--bubble--value' )
          .attr( 'x', detailWidth / 2 )
          .attr( 'y', detailHeight / 4 * 3 )
          .attr( 'text-anchor', 'middle' )
          .text( data.value );
    }
    
    function tween( b, callback ) {
      return function( a ) {
        var i = (function interpolate() {
          return function( t ) {
            return a.map( function( datum, index ) {
              return {
                date  : datum.date,
                value : datum.value + b[ index ].value * t
              };
            } ); 
          };
        })();
  
        return function( t ) {
          return callback( i ( t ) );
        };
      };
    }
  }

  function svgSHOW() {
    drawLineChart(    'lineChart',    data.lineChart );
  }

  // yeah, let's kick things off!!!
    svgSHOW();
})();