import React, { Component } from "react";
import {
  PdfLoader,
  PdfHighlighter,
  Tip,
  Highlight,
  Popup,
  AreaHighlight,
} from "./react-pdf-highlighter";
import type { IHighlight, NewHighlight, Scaled } from "./react-pdf-highlighter";
// import { testHighlights as _testHighlights } from "./test-highlights";
import { Spinner } from "./Spinner";
import { Sidebar } from "./Sidebar";
import "./style/App.css";
import { getDocument, GlobalWorkerOptions, version } from 'pdfjs-dist';
import { TextItem } from "pdfjs-dist/types/src/display/api";
// import { text } from "stream/consumers";
// import { start } from "repl";
// import { text } from "stream/consumers";

// 设置 PDF.js worker
GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${version}/pdf.worker.js`;


// const testHighlights: Record<string, Array<IHighlight>> = _testHighlights;

interface State {
  url: string;
  highlights: Array<IHighlight>;
  question: string;
  model_name: string;
  baseline_type: string;
  raw_provenance: Array<string>;
  evidence: Array<string>;
  raw_answer: string;
  evidence_answer: string;
  search_pool: Array<string>;
}

const getNextId = () => String(Math.random()).slice(2);

const parseIdFromHash = () => document.location.hash.slice("#highlight-".length);

const resetHash = () => {
  document.location.hash = "";
};

const HighlightPopup = ({
  comment,
}: {
  comment: { text: string; emoji: string };
}) =>
  comment.text ? (
    <div className="Highlight__popup">
      {comment.emoji} {comment.text}
    </div>
  ) : null;

// const PRIMARY_PDF_URL = "https://arxiv.org/pdf/1708.08021.pdf";

class App extends Component<{}, State> {
  state: State = {
    url: "",
    highlights: [],
    question: "",
    model_name: "",
    baseline_type: "",
    raw_provenance: [],
    evidence: [],
    raw_answer: "",
    evidence_answer: "",
    search_pool: [],
  };

  componentDidMount() {
    // this.fetchDocumentPath();
    // this.fetchJsonPath();
    window.addEventListener("hashchange", this.scrollToHighlightFromHash, false);
    
  }

  fetchJsonPath = async (fileName: String) => {
    console.log("fileName:", fileName);
    try {
      const response = await fetch(`data/${fileName}.json`);
      const data = await response.json();
      const { model_name, baseline_type, document_path, question, raw_provenance, evidence, raw_answer, evidence_answer, search_pool } = data;


      if (document_path) {
        this.setState({
          url: document_path.trim(),
          // highlights: testHighlights[document_path] ? [...testHighlights[document_path]] : [],
          question: question || "",
          model_name: model_name || "",
          baseline_type: String(baseline_type) || "",
          raw_provenance: raw_provenance || [],
          evidence: evidence || [],
          raw_answer: raw_answer || "",
          evidence_answer: evidence_answer || "",
          search_pool: search_pool || [],
        }, () => {
          this.highlightTexts(raw_provenance);
        });
      }
      
    } catch (error) {
      console.error("Error fetching document path:", error);
    }
  };



  highlightTexts = async (chunks: Array<string>) => {
    console.log("chunks:", chunks);
    // const emoji_list = ["1🔍", "2👀", "3💩"]
    try {
      const pdf = await getDocument(this.state.url).promise;
      
      chunks.forEach(async (docArray, docArrayIndex) => { // for different model_name's retrival
        // docArray.forEach(async (doc, docIndex) => { // for each retrieved chunk
        // console.log("doc:", doc[0]);
        
        let docTextOriginal = docArray; // docText is a string
        this.ScanToHighlightChunk(pdf, docTextOriginal, docArrayIndex);
      });



  } catch (error) {
    console.error("Error in highlightRetrievedTexts:", error);
  }
};


  addHighlight = (highlight: NewHighlight) => {
    console.log("Saving highlight", highlight);
  
    this.setState((prevState) => ({
      highlights: [{ ...highlight, id: getNextId() }, ...prevState.highlights],
    }), () => {
    });
  };
  
  

  scrollViewerTo = (highlight: any) => { };

  scrollToHighlightFromHash = () => {
    const highlight = this.getHighlightById(parseIdFromHash());

    if (highlight) {
      this.scrollViewerTo(highlight);
    }
  };

  getHighlightById(id: string) {
    const { highlights } = this.state;
    return highlights.find((highlight) => highlight.id === id);
  }

  updateHighlight(highlightId: string, position: Object, content: Object, comment: Object) {
    console.log("Updating highlight", highlightId, position, content);
    this.setState({
      highlights: this.state.highlights.map((h) => {
        const { id, position: originalPosition, content: originalContent, comment: originalComment, ...rest } = h;
        return id === highlightId
          ? {
            id,
            position: { ...originalPosition, ...position },
            content: { ...originalContent, ...content },
            comment: { ...originalComment, ...comment },
            ...rest,
          }
          : h;
      }),
    });
  }

  getExistingHighlights = () => {
    console.log("Existing Highlights:");
    const { highlights } = this.state;
    highlights.forEach((highlight) => {
      console.log('Existing Highlight:', highlight);
    });
  };

  getHighlightArea = (startIndex: number, endIndex: number, textItems: any) => {
    let highlightArea = [];
    let y1 = textItems[startIndex].transform[5];
    let y1_1 = y1+textItems[startIndex].height;
    let y2 = textItems[startIndex].transform[5];
    let x1 = textItems[startIndex].transform[4];
    let x2 = textItems[startIndex].transform[4] + textItems[startIndex].width;

    for (let i = startIndex; i < endIndex; i++) {
      if (textItems[i].transform[5] <= y1) { // go to button more
        y2 = textItems[i].transform[5];
        // console.log("y2:", y2);
        // y1 = textItems[startIndex].transform[5];
        x1 = Math.min(x1, textItems[i].transform[4]);
        x2 = Math.max(x2, textItems[i].transform[4] + textItems[i].width);
        y1_1 = Math.max(y1+textItems[i].height, y1_1)
      }
      else {
        
        highlightArea.push([x1, y1_1, x2, y2]);
        
        y1 = textItems[i].transform[5];
        y1_1 = y1+textItems[startIndex].height;
        y2 = textItems[i].transform[5];
        x1 = textItems[i].transform[4];
        x2 = textItems[i].transform[4] + textItems[i].width;
      }
    }
    highlightArea.push([ x1, y1_1, x2, y2 ]);
    return highlightArea;
  }

  ScanToHighlightChunk = async (pdf: any, pattern: string, patternIndex: number) => {
    pattern = pattern.replace(/\(cid:\d+\)/g, "")
    
    let highlightArea: number [][] = [];
    let lastPageHighlightArea: number[][] = [];
    
    

    let highlightAreaTexts = [];
    let highlightAreaPureTexts = '';
    // let lastPageHighlightTexts = [];
    let lastPageHighlightPureTexts = '';

    // let highlightStartIndex = null;
    // let highlightEndIndex = null;
    
    for (let i = 0; i < pdf.numPages; i++) {
      let docPage = i+1;
      let page = await pdf.getPage(docPage);
      let textContents = await page.getTextContent();
      let textItemsUnsorted = textContents.items;
      
      
      const startIndex = 0;
      const textItems = textItemsUnsorted.sort((a: TextItem, b: TextItem) => {
        if (a.transform[4] === b.transform[4]) {
            return b.transform[5] - a.transform[5];
        } else {
            return a.transform[4] - b.transform[4];
        }
    });
      const endIndex = textItems.length;
      // console.log("textItemsLength:", endIndex);
      // console.log("textItems:", textItems);
      const y1Start = textItems[startIndex].transform[5];
      const y1_1Start = y1Start + textItems[startIndex].height;
      const y2Start = textItems[startIndex].transform[5];
      const x1Start = textItems[startIndex].transform[4];
      const x2Start = textItems[startIndex].transform[4] + textItems[startIndex].width;
      // const y1End = textItems[endIndex - 1].transform[5];
      // const y1_1End = y1End + textItems[endIndex - 1].height;
      // const y2End = textItems[endIndex - 1].transform[5];
      // const x1End = textItems[endIndex - 1].transform[4];
      // const x2End = textItems[endIndex - 1].transform[4] + textItems[endIndex - 1].width;

      let y1 = y1Start;
      let y1_1 = y1_1Start;
      let y2 = y2Start;
      let x1 = x1Start;
      let x2 = x2Start;
    
      let pureStrPattern = pattern.replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
      // console.log("pureStrPattern:", pureStrPattern);
      // console.log("pattern:", pattern);
      let lineStartIndex = startIndex;
      let lineEndIndex = startIndex;
      // let highLightFlag = false;
      let successType = 0;
      // let noHighLightFlag = false;
      for (let i = startIndex; i < endIndex; i++) {
        if (textItems[i].transform[5] != y1 || i == endIndex - 1) { // go to button more
          
          lineEndIndex = i - 1;
          let lineText = textItems.slice(lineStartIndex, i).map((item: TextItem) => item.str).join('');
          if (i == endIndex - 1) {
            lineEndIndex = i;
            lineText = textItems.slice(lineStartIndex, endIndex).map((item: TextItem) => item.str).join('');
          }
          let pureStrLineText = lineText.replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
          // console.log("pureStrLineText:", pureStrLineText);
          if (pureStrPattern.includes(pureStrLineText)) { // line text is in pattern
            x1 = textItems[lineStartIndex].transform[4];
            x2 = textItems[lineEndIndex].transform[4] + textItems[lineEndIndex].width;
            y1 = textItems[lineStartIndex].transform[5];
            y1_1 = y1 + textItems[lineEndIndex].height;
            y2 = textItems[lineEndIndex].transform[5];
            highlightArea.push([x1, y1_1, x2, y2]);
            // pureStrPattern.replace(pureStrLineText, '');
            // console.log("pureStrPattern:", pureStrPattern);
            // console.log("pattern", pattern);
            // console.log("pureStrLineText:", pureStrLineText);
            // console.log("lineStartIndex:", lineStartIndex);
            // console.log("lineEndIndex:", i);
            highlightAreaTexts.push(lineText);
            // highLightFlag = true;
            if (i == endIndex - 1) { //case 3
              highlightAreaPureTexts = highlightAreaTexts.join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
              let highlightStartIndex = 0;
              let highlightEndIndex = i;
              for (let j = 1; j < highlightAreaTexts.length; j++) {
                console.log("j:", j)
                if (highlightAreaTexts.slice(j).join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase().slice(0, 3) == pureStrPattern.slice(0, 3)) {
                  console.log("highlighttext3: ",highlightAreaTexts.slice(j).join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase())
                  console.log("strpattern3: ", pureStrPattern)
                  highlightStartIndex = j;
                  break;
                }
              }
              highlightAreaTexts = highlightAreaTexts.slice(highlightStartIndex, highlightEndIndex);
                  highlightAreaPureTexts = highlightAreaTexts.join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
                  highlightArea = highlightArea.slice(highlightStartIndex, highlightEndIndex);
              if (highlightAreaPureTexts.includes(pureStrPattern) || this.compareCharFrequency(highlightAreaPureTexts, pureStrPattern, 0.8)) { // success
                // if (highlightAreaPureTexts.length != pureStrPattern.length) {
                  

                //   // for (let j = highlightAreaTexts.length; j >= 0; j--) {
                //   //   if (!highlightAreaTexts.slice(0, j).join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase().includes(pureStrPattern)) {
                //   //     highlightEndIndex = j + 1;
                //   //     break;
                //   //   }
                //   // }
                //   // console.log("highlightStartIndex:", highlightStartIndex);
                //   // console.log("highlightEndIndex:", highlightEndIndex);
                //   // console.log("highlightLength:", highlightAreaTexts.length);

                  
                // }
                
                successType = 3;
                for (let evidenceElement of this.state.evidence) {
                  this.ScanToHighlightRow(page, textItems, evidenceElement, startIndex, endIndex, docPage);
                }
                // console.log("successType:", successType);
                // console.log("lastPageHighlightPureTexts:", lastPageHighlightPureTexts);
                // console.log("highlightAreaPureTexts:", highlightAreaPureTexts);
                // console.log("pureStrPattern:", pureStrPattern);
                break;
              }
              
              console.log("highlightAreaTexts:", highlightAreaTexts);
              // lastPageHighlightTexts = highlightAreaTexts;
              lastPageHighlightArea = highlightArea;
              lastPageHighlightPureTexts = highlightAreaPureTexts;
              highlightArea = [];
              highlightAreaTexts = [];
              highlightAreaPureTexts = '';
              // next page
            }
          }
          else if (highlightArea.length > 0) { // line text is not in pattern
            // console.log("Existing Texts:", highlightArea.map(item => textItems.slice(item[0], item[2]).map(item => item.str).join('')).join(''));
            // console.log("highlights:", highlightArea);
            if (highlightArea[0][0] == x1Start && highlightArea[0][3] == y2Start) { //case 1
              // console.log("case 1")
              highlightAreaPureTexts = highlightAreaTexts.join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
              console.log("lastPageHighlightPureTexts:", lastPageHighlightPureTexts)
              console.log("highlightAreaPureTexts:", highlightAreaPureTexts);
              console.log("pureStrPattern:", pureStrPattern);
              if ((lastPageHighlightPureTexts + highlightAreaPureTexts).includes(pureStrPattern) || this.compareCharFrequency(lastPageHighlightPureTexts + highlightAreaPureTexts, pureStrPattern, 0.8)) { // success
                if ((lastPageHighlightPureTexts + highlightAreaPureTexts).length != pureStrPattern.length) {
                  let highlightStartIndex = 0;
                  let highlightEndIndex = i;
                  for (let j = 1; j < highlightAreaTexts.length; j++) {
                    if (!highlightAreaTexts.slice(j).join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase().includes(pureStrPattern)) {
                      highlightStartIndex = j - 1;
                      break;
                    }
                  }
                  for (let j = highlightAreaTexts.length; j >= 0; j--) {
                    if (!highlightAreaTexts.slice(0, j).join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase().includes(pureStrPattern)) {
                      highlightEndIndex = j + 1;
                      break;
                    }
                  }

                  // console.log("highlightStartIndex:", highlightStartIndex);
                  // console.log("highlightEndIndex:", highlightEndIndex);
                  // console.log("highlightLength:", highlightAreaTexts.length);

                  highlightAreaTexts = highlightAreaTexts.slice(highlightStartIndex, highlightEndIndex);
                  highlightAreaPureTexts = highlightAreaTexts.join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
                  highlightArea = highlightArea.slice(highlightStartIndex, highlightEndIndex);
                }
                
                successType = 1;
                for (let evidenceElement of this.state.evidence) {
                  if (docPage > 1) {
                    const lastPage = await pdf.getPage(docPage - 1);
                    const lastTextContents = await lastPage.getTextContent();
                    const lastTextItemsUnsorted = lastTextContents.items;
                    const lastTextItems = lastTextItemsUnsorted.sort((a: TextItem, b: TextItem) => b.transform[5] - a.transform[5]);
                    const lastPageStartIndex = 0;
                    const lastPageEndIndex = lastTextItems.length;
                    this.ScanToHighlightRow(lastPage, lastTextItems, evidenceElement, lastPageStartIndex, lastPageEndIndex, docPage - 1);
                  }
                  this.ScanToHighlightRow(page, textItems, evidenceElement, startIndex, endIndex, docPage);
                }
                // console.log("successType:", successType);
                // console.log("lastPageHighlightPureTexts:", lastPageHighlightPureTexts);
                // console.log("highlightAreaPureTexts:", highlightAreaPureTexts);
                // console.log("pureStrPattern:", pureStrPattern);
                break;
              }
              // fail
              highlightArea = [];
              lastPageHighlightArea = [];
              highlightAreaTexts = [];
              // lastPageHighlightTexts = [];
              highlightAreaPureTexts = '';
              lastPageHighlightPureTexts = '';
              continue;
            }
            else { // case 2
              // console.log("case 2")
              highlightAreaPureTexts = highlightAreaTexts.join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
              // console.log("highlightAreaPureTexts:", highlightAreaPureTexts);
              if (highlightAreaPureTexts.includes(pureStrPattern) || this.compareCharFrequency(highlightAreaPureTexts, pureStrPattern, 0.8)) { // success
                if (!this.compareCharFrequency(highlightAreaPureTexts, pureStrPattern, 0.95)) {
                  let highlightStartIndex = 0;
                  let highlightEndIndex = i;
                  for (let j = 1; j < highlightAreaTexts.length; j++) {
                    if (!highlightAreaTexts.slice(j).join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase().includes(pureStrPattern)) {
                      highlightStartIndex = j - 1;
                      break;
                    }
                  }
                  for (let j = highlightAreaTexts.length; j >= 0; j--) {
                    if (!highlightAreaTexts.slice(0, j).join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase().includes(pureStrPattern)) {
                      highlightEndIndex = j + 1;
                      break;
                    }
                  }

                  // console.log("highlightStartIndex:", highlightStartIndex);
                  // console.log("highlightEndIndex:", highlightEndIndex);
                  // console.log("highlightLength:", highlightAreaTexts.length);

                  highlightAreaTexts = highlightAreaTexts.slice(highlightStartIndex, highlightEndIndex);
                  highlightAreaPureTexts = highlightAreaTexts.join('').replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
                  highlightArea = highlightArea.slice(highlightStartIndex, highlightEndIndex);
                }

                successType = 2;
                for (let evidenceElement of this.state.evidence) {
                  this.ScanToHighlightRow(page, textItems, evidenceElement, startIndex, endIndex, docPage);
                }
                // console.log("successType:", successType);
                // console.log("lastPageHighlightPureTexts:", lastPageHighlightPureTexts);
                // console.log("highlightAreaPureTexts:", highlightAreaPureTexts);
                // console.log("pureStrPattern:", pureStrPattern);
                break;
              }
              highlightArea = [];
              lastPageHighlightArea = [];
              highlightAreaTexts = [];
              // lastPageHighlightTexts = [];
              highlightAreaPureTexts = '';
              lastPageHighlightPureTexts = '';
              continue;
              // noHighLightFlag = true;
            }
          }
          y1 = textItems[i].transform[5];
          lineStartIndex = i;
        }
      }
      // end of page
      if (successType == 2 || successType == 3) {
        this.setHighlightArea(highlightArea, page, docPage, pattern, patternIndex);
        break;
      }
      if (successType == 1) {
        this.setHighlightArea(lastPageHighlightArea, page, docPage - 1, pattern, patternIndex);
        this.setHighlightArea(highlightArea, page, docPage, pattern, patternIndex);
        break;
      }
    }
    // const result = highlightArea.concat(lastPageHighlightArea);
    // console.log("result:", result);
    // return result;
    
  }

  ScanToHighlightRow = async (page: any, textItems: any, pattern: string, startIndex: number, endIndex: number, docPage: number) => {
    pattern = pattern.replace(/\(cid:\d+\)/g, "")
    let patternPure = pattern.replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
    let highlightAllText = textItems.slice(startIndex, endIndex).map((item: TextItem) => item.str).join('');
    let highlightPureText = highlightAllText.replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
    // console.log("highlightAllText:", highlightAllText);
    //   console.log("pattern:", pattern);
    if (highlightPureText.includes(patternPure) || this.compareCharFrequency(highlightPureText, patternPure, 0.65)) {
      
      let highlightStartIndex = 0;
      let highlightEndIndex = 0;
      for (let i = startIndex; i < endIndex; i++) {
        let highlightTexts = textItems.slice(i, endIndex).map((item: TextItem) => item.str).join('');
        let highlightPureTexts = highlightTexts.replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
        if (!highlightPureTexts.includes(patternPure)) {
          highlightStartIndex = i - 1;
          break;
        }
      }
      for (let i = endIndex - startIndex; i >= 0; i--) {
        let highlightTexts = textItems.slice(startIndex, startIndex + i).map((item: TextItem) => item.str).join('');
        let highlightPureTexts = highlightTexts.replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
        if (!highlightPureTexts.includes(patternPure)) {
          highlightEndIndex = i + 1;
          break;
        }
      }
      let highlightArea = [];
      let y1 = textItems[highlightStartIndex].transform[5];
      let y1_1 = y1+textItems[highlightStartIndex].height;
      let y2 = textItems[highlightStartIndex].transform[5];
      let x1 = textItems[highlightStartIndex].transform[4];
      let x2 = textItems[highlightStartIndex].transform[4] + textItems[highlightStartIndex].width;
      for (let i = highlightStartIndex; i < highlightEndIndex; i++) {
        x1 = textItems[i].transform[4];
        x2 = textItems[i].transform[4] + textItems[i].width;
        y1 = textItems[i].transform[5];
        y1_1 = y1 + textItems[i].height;
        y2 = textItems[i].transform[5];
        highlightArea.push([x1, y1_1, x2, y2]);
      }
      this.setHighlightRow(highlightArea, page, docPage, pattern, 0);
    }
  }

  setHighlightArea = (highLightArea: any, page: any, pageNum: number, chunkText: string, chunkIndex: number) => {
    if (highLightArea.length == 0) {
      return;
    }
    const viewport = page.getViewport({ scale: 1 });
    let x1 = highLightArea[0][0];
    let y1 = highLightArea[0][1];
    let x2 = highLightArea[0][2];
    let y2 = highLightArea[0][3];
    for (let k = 0; k < highLightArea.length; k++) {
      x1 = Math.min(x1, highLightArea[k][0]);
      y1 = Math.max(y1, highLightArea[k][1]);
      x2 = Math.max(x2, highLightArea[k][2]);
      y2 = Math.min(y2, highLightArea[k][3]);
    }
    const startCoords = viewport.convertToPdfPoint(x1, y1);
    const endCoords = viewport.convertToPdfPoint(x2, y2);
    let boundingRect = {
      height: viewport.height,
      width: viewport.width,
      x1: startCoords[0],
      y1: startCoords[1],
      x2: endCoords[0],
      y2: endCoords[1],
    }
            
    this.addHighlight({
      position: {
        boundingRect,
        rects: [boundingRect],
        pageNumber: pageNum,
      },
      content: {
        text: chunkText,
      },
      comment: {
        text: "Top" + String(chunkIndex+1),
        emoji: "",
      }
    });
  }

  setHighlightRow = (highLightArea: any, page: any, pageNum: number, chunkText: string, chunkIndex: number) => {
    const viewport = page.getViewport({ scale: 1 });
    for (let k = 0; k < highLightArea.length; k++) {
      let x1 = highLightArea[k][0];
      let y1 = highLightArea[k][1];
      let x2 = highLightArea[k][2];
      let y2 = highLightArea[k][3];
      const startCoords = viewport.convertToPdfPoint(x1, y1);
    const endCoords = viewport.convertToPdfPoint(x2, y2);
    let boundingRect = {
      height: viewport.height,
      width: viewport.width,
      x1: startCoords[0],
      y1: startCoords[1],
      x2: endCoords[0],
      y2: endCoords[1],
    }
            
    this.addHighlight({
      position: {
        boundingRect,
        rects: [boundingRect],
        pageNumber: pageNum,
      },
      content: {
        text: chunkText,
      },
      comment: {
        text: "",
        emoji: "",
      }
    });
    }
  }


  convertTextPositionToBoundingRect = (startPosition:any, endPosition:any , page: any): Scaled => {
    if (!startPosition || !endPosition || !startPosition.transform || !endPosition.transform) {
      console.error("Invalid startPosition or endPosition", startPosition, endPosition);
      
    }
  
    const viewport = page.getViewport({ scale: 1 });
    
    // 提取变换矩阵中的坐标信息
    const startCoords = viewport.convertToPdfPoint(startPosition.transform[4], startPosition.transform[5]);
    const endCoords = viewport.convertToPdfPoint(startPosition.transform[4] + startPosition.width, startPosition.transform[5] - startPosition.height);
  
    // 计算边界矩形
    const boundingRect: Scaled = {
      x1: 0,
      y1: startCoords[1]-8.5, //idk why -8.5 is needed
      x2: viewport.width,
      y2: endCoords[1]-8.5,
      width: viewport.width, //width is page width
      height: viewport.height, //height is page height
      pageNumber: page.pageNumber
    };
  
    return boundingRect;
  };
  
  handleFileSubmit = (fileName: string) => {
    this.fetchJsonPath(fileName);
  };

  charFrequency(str: string) {
    let frequency: Record<string, number> = {};
  
    for (const char of str) {
      frequency[char] = (frequency[char] || 0) + 1;
    }
  
    return frequency;
  }
  
  compareCharFrequency(str1: string, str2: string, threshold = 0.9) {
    const freq1 = this.charFrequency(str1);
    const freq2 = this.charFrequency(str2);
  
    const allChars = new Set([...Object.keys(freq1), ...Object.keys(freq2)]);
    let totalChars = 0;
    let matchingChars = 0;
  
    allChars.forEach((char) => {
      const count1 = freq1[char] || 0;
      const count2 = freq2[char] || 0;
      totalChars += Math.max(count1, count2);
      matchingChars += Math.min(count1, count2);
    });
  
    const similarity = matchingChars / totalChars;
    // console.log("similarity:", similarity);
    return similarity >= threshold;
  }

  // fuzzyMatchWithIndices(text:String, pattern:String, threshold = 10) {
  //   const tLen = text.length;
  //   const pLen = pattern.length;

  //   if (tLen < pLen) return null;

  //   let bestDistance = Infinity;
  //   let bestIndices = null;

  //   for (let i = 0; i <= tLen - pLen; i++) {
  //       const substring = text.slice(i, i + pLen);
  //       const distanceMatrix = this.levenshteinDistance(substring, pattern);
  //       const distance = distanceMatrix[pLen][pLen];

  //       if (distance <= threshold && distance < bestDistance) {
  //           bestDistance = distance;
  //           bestIndices = [i, i + pLen - 1];
  //       }
  //   }

  //   return bestIndices;
  // }

  fuzzyMatchWithIndices(text: String, pattern: String, threshold = 0.9) {
    const tLen = text.length;
    const pLen = pattern.length;
    
    if (tLen < pLen) return null;

    let bestMatch = { score: 0, startIndex: -1, endIndex: -1 };

    for (let i = 0; i <= tLen - pLen; i++) {
        const substring = text.slice(i, i + pLen);
        // let matchScore = 0;

        // for (let j = 0; j < pLen; j++) {
        //     if (substring.slice(Math.max(0, j-3), Math.min(j+3, pLen)).includes(pattern[j])) {
        //         matchScore++;
        //     }
        // }

      // const score = matchScore / pLen;
      const score = this.jaccardSimilarity(substring, pattern);

        if (score > bestMatch.score) {
            bestMatch = { score, startIndex: i, endIndex: i + pLen - 1 };
        }

        if (score >= threshold) {
            return bestMatch;
        }
    }

    return bestMatch.score >= threshold ? bestMatch : null;
  }
  
  getCharacterSet(str: String) {
    return new Set(str);
  }

  jaccardSimilarity(str1:String, str2:String) {
    const set1 = this.getCharacterSet(str1);
    const set2 = this.getCharacterSet(str2);

    const intersection = new Set([...set1].filter(char => set2.has(char)));
    const union = new Set([...set1, ...set2]);

    return intersection.size / union.size;
  }


  render() {
    const { url, highlights, question, model_name, baseline_type, raw_answer, evidence_answer, search_pool, evidence } = this.state;

    return (
      <div className="App" style={{ display: "flex", height: "100vh" }}>
        <Sidebar
          // highlights={highlights}
          // resetHighlights={this.resetHighlights}
          // toggleDocument={this.toggleDocument}
          question={question}
          model_name={model_name}
          baseline_type={baseline_type}
          raw_answer={raw_answer}
          evidence_answer={evidence_answer}
          search_pool={String(search_pool)}
          evidence={String(evidence)}
          onFileSubmit={this.handleFileSubmit}
        />
        <div style={{ height: "100vh", width: "75vw", position: "relative" }}>
          {url ? (
            <PdfLoader url={url} beforeLoad={<Spinner />}>
              {(pdfDocument) => (
                <PdfHighlighter
                  pdfDocument={pdfDocument}
                  enableAreaSelection={(event) => event.altKey}
                  onScrollChange={resetHash}
                  scrollRef={(scrollTo) => {
                    this.scrollViewerTo = scrollTo;
                    this.scrollToHighlightFromHash();
                  }}
                  onSelectionFinished={(position, content, hideTipAndSelection, transformSelection) => (
                    <Tip
                      onOpen={transformSelection}
                      onConfirm={(comment) => {
                        this.addHighlight({ content, position, comment });
                        hideTipAndSelection();
                      }}
                    />
                  )}
                  highlightTransform={(highlight, index, setTip, hideTip, viewportToScaled, screenshot, isScrolledTo) => {
                    const isTextHighlight = !Boolean(highlight.content && highlight.content.image);
                    const component = isTextHighlight ? (
                      <Highlight isScrolledTo={isScrolledTo} position={highlight.position} comment={highlight.comment} />
                    ) : (
                      <AreaHighlight
                        isScrolledTo={isScrolledTo}
                        highlight={highlight}
                        onChange={(boundingRect) => {
                          this.updateHighlight(
                            highlight.id,
                            { boundingRect: viewportToScaled(boundingRect) },
                            { image: screenshot(boundingRect) },
                            {}
                          );
                        }}
                      />
                    );
                    return (
                      <Popup
                        popupContent={<HighlightPopup {...highlight} />}
                        onMouseOver={(popupContent) => setTip(highlight, (highlight) => popupContent)}
                        onMouseOut={hideTip}
                        key={index}
                        children={component}
                      />
                    );
                  }}
                  highlights={highlights}
                />
              )}
            </PdfLoader>
          ) : (
            <Spinner />
          )}
        </div>
      </div>
    );
  }
}

export default App;


