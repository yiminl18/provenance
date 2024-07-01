

import Graph from "react-graph-vis";
import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import { Node } from "../classes/Node.ts"
import { Edge } from "../classes/Edge.ts"
import { Link } from "react-router-dom";
import './App.css';

var allNodes = [];
var allEdges = [];
var rerender = true

const options = {
  layout: {
    hierarchical: false
  },
  edges: {
    color: "#000000"
  },
  height: '108%',
};


function fetchJSONData() {
  // const fetchJsonData = require('../testData/mockData4.json');
  const fetchJsonData = require('../testData/mockData10.json');
  // const fetchJsonData = require('../testData/mockData50.json');
  // const fetchJsonData = require('../testData/node_info.json');
  // const fetchJsonData = require('../testData/zenDBsql1paper.json');
  createNodes(fetchJsonData)
  createEdges(fetchJsonData)
}

const createNodes = (data) => {
  for (const nodeTitle in data) {

    var createdNode = new Node( data[nodeTitle].node_id, data[nodeTitle].node_name, 
      data[nodeTitle].in_nodes, data[nodeTitle].out_nodes, data[nodeTitle].in_data, data[nodeTitle].out_data, data[nodeTitle].label, data[nodeTitle].prompt)   
  
    allNodes.push(createdNode)
  }
};

const createEdges = (data) => {
  for (const nodeTitle in data) {
    data[nodeTitle].out_nodes.forEach(outGoingId => {
      
      var createdEdge = new Edge(data[nodeTitle].node_id, outGoingId)   
      allEdges.push(createdEdge) 
    });
  }
};


const App = () => {
  const [selectedNode, setSelectedNode] = useState("");
  var combinedStringOutout = "";
  var combinedStringIndex = "";

  useEffect(() => {
    if (rerender == true){
      console.log("began fetching for json data")
      fetchJSONData();
      rerender = false
    }
    else{
      console.log("already rendered")
    }

  }, []);


  const FormattedContent = ({ content }) => {
    return (
      <div dangerouslySetInnerHTML={{ __html: content }} />
    );
  };

  const [state, setState] = useState({
    counter: 5,
    graph: {
      nodes:allNodes.map((node) => ({
        id: node.id,
        label: node.name,
        color: "#ADD8E6",
      })),
      edges:allEdges.map((edge) => ({
        from: edge.inComingId,
        to: edge.outGoingId,
      })),
    },
    events: {
      select: ({ nodes, edges }) => {
        allNodes.forEach(currentNode =>{
         if (currentNode.id == nodes){
          setSelectedNode(currentNode)
         }
        }) 
      }
    }
  })
  
  const { graph, events } = state;

  const getNodeNameById = (id) => {
    const node = allNodes.find((node) => node.id === id);
    return node ? node.name : 'Nowhere';
  };

  return (
    <div id="webPage">
      <h1 id="webPageTitle">Node Interface</h1>
      
      <div id="theGraph">
        <Graph graph={graph} options={options} events={events} style={{ height: "100%" }}/>
      </div>
  
      <section id="NodeInfoSection">
        <section id="NodeNameandPrompt">
          <div id="ClickedNodeTitle"><b>Selected Node: </b>{selectedNode.name}</div>
          <div id="ClickedNodePrompt"><b>Prompt: </b> {selectedNode.prompt !== "" ? selectedNode.prompt : "There is no prompt"}</div>
        </section>
  
        <section id="InComingDataContainer">
          <section id="InComingDateTitleandLink">
            <div id="InComingDateTitle"><b>In-Coming Data:</b></div>
            <div className="outerLinkTextandLink">
              Orginal Source:
              <a href="https://google.com" class="button" className="outerLink"></a>
            </div>

          </section>
          <section id="InComingDataBoxes">
            {selectedNode.inData && selectedNode.inData.map((data, index) => (
              <div key={index} className="dataBox">From {getNodeNameById(selectedNode.inNodes[index])}: <FormattedContent content={selectedNode.formatDataWithNewlines(data)}/>
              </div>
            ))}
          </section>
        </section>
  
        <section id="OutGoingDataContainer">
        <section id="OutGoinggDateTitleandLink">
            <div id="OutGoingDataTitle"><b>Out-Going Data:</b></div>
            <div className="outerLinkTextandLink">
                Orginal Source:
                <a href="http://localhost:3000/react-pdf-highlighter/" class="button" className="outerLink"></a>
              </div>
        </section>
          <section id="OutGoingDataBoxes">
            {selectedNode.outData && typeof selectedNode.outData[0] === "string" && selectedNode.outData.map((data, index) => (
              <div key={index} className="dataBox">To {getNodeNameById(selectedNode.outNodes[index])}: <FormattedContent content={selectedNode.formatDataWithNewlines(data)}/>
              </div>
            ))}
  
            {selectedNode.outData && Array.isArray(selectedNode.outData[0]) &&
              selectedNode.outData.map((nestedList, nestedIndex) =>
                nestedList.map((element, index) => {
                  if (index === 0) {
                    combinedStringOutout += selectedNode.formatDataWithNewlines(element);
                    combinedStringIndex = getNodeNameById(selectedNode.outNodes[index]);
                  }
                  return null; 
                })
              )
            }

            {combinedStringIndex != "" && <div className="dataBox">To {combinedStringIndex}: <FormattedContent content ={combinedStringOutout}/>
            <div id="outerLink"></div>
            </div>
            }
          </section>
        </section>
      </section>
    </div>
  );

}

ReactDOM.render(
  <App />,
  document.getElementById("root")
);

export default App;

