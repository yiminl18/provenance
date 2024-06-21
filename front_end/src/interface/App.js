

import Graph from "react-graph-vis";
import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import { Node } from "../classes/Node.ts"
import { Edge } from "../classes/Edge.ts"
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
  // const fetchJsonData = require('../testData/mockData10.json');
  const fetchJsonData = require('../testData/node_info.json');
  //const fetchJsonData = require('../testData/zenDBsql1.json');
  createNodes(fetchJsonData)
  createEdges(fetchJsonData)
}

const createNodes = (data) => {
  for (const nodeTitle in data) {

    var createdNode = new Node( data[nodeTitle].node_id, data[nodeTitle].node_name, 
      data[nodeTitle].in_nodes, data[nodeTitle].out_nodes, data[nodeTitle].in_data, data[nodeTitle].out_data)   
  
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
        <Graph graph={graph} options={options} events={events} style={{ height: "640px" }}/>
      </div>
      <section id="NodeInfoSection">
        <div id="ClickedNodeTitle"><b>Selected Node:</b> {selectedNode.name}</div>
        <div id="InComingDataContainer"><b>In-Coming Data:</b>
        {selectedNode.inData && selectedNode.inData.map((data, index) => (
            <div key={index} className="dataBox">From {getNodeNameById(selectedNode.inNodes[index])}: {data}</div>
          ))}</div>
        <div id="OutGoingDataContainer"><b>Out-Going Data:</b>  
        {selectedNode.outData && selectedNode.outData.map((data, index) => (
            <div key={index} className="dataBox">To {getNodeNameById(selectedNode.outNodes[index])}: {data}</div>
          ))}</div>
      </section>
      
    </div>
  );

}

ReactDOM.render(
  <App />,
  document.getElementById("root")
);

export default App;

