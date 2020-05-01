/************************************************************************************************************************
 * Project  : Plot graph by getting data through Flask API
 * Author   : Shobhit Gupta
 * Date     : 1st May 2020
 ************************************************************************************************************************/

 // importing the libraries
import React from 'react';
import { render } from 'react-dom';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import axios from 'axios'

// function to fetch graph configuration
const getConfig = mydata =>({
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Distribution of Titles across Years'
    },
    subtitle: {
        text: 'on Wikipages data'
    },
    xAxis: {
        categories: mydata.labels, 
        title: {
            text: null
        }
    }, 
    yAxis: {
        min: 0,
        title: {
            text: 'No of Titles'
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
        valueSuffix: ' titles'
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true
            }
        }
    },
    
    credits: {
        enabled: false
    },
    series: [{
        name: 'Years',
        data: mydata.counts 
    }]
})



class App extends React.Component{

    
    constructor(props) {  
        
        super(props);  

        this.state = {
            dataResults: {},
          }  
        
    }

    getData = () => {
        axios.get('http://localhost:2010/get_data')
          .then(res => {
            this.setState({
              dataResults: res.data
            });
            console.log(res)
          })
          .catch(error => {
              this.setState({
                  dataResults : {'counts':[0],'labels':['No data']}
              });
          });
        }


        componentDidMount() {
            this.getData();
          }  // end of componentMount

    render(){
        const { dataResults } = this.state;
        const chartConfig = getConfig(dataResults);

        return(
            <div>
                <h1> React App for showing graph</h1>
                <h2> Author : Shobhit Gupta</h2>
                <HighchartsReact highcharts={Highcharts} options={chartConfig} />
            </div>
        );
    }

}

  render(<App />, document.getElementById('root'));