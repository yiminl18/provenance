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
// import { start } from "repl";
// import { text } from "stream/consumers";

// 设置 PDF.js worker
GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${version}/pdf.worker.js`;


// const testHighlights: Record<string, Array<IHighlight>> = _testHighlights;

interface State {
  url: string;
  highlights: Array<IHighlight>;
  question: string;
  sub_query: Array<string>;
  sub_answers: Array<string>;
  chunks: Array<Array<string>>;
  finalAnswer: string;
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
    sub_query: [],
    sub_answers: [],
    chunks: [],
    finalAnswer: "",
  };

  componentDidMount() {
    // this.fetchDocumentPath();
    // this.fetchJsonPath();
    window.addEventListener("hashchange", this.scrollToHighlightFromHash, false);
    
  }

  fetchJsonPath = async (fileName: String) => {
    console.log("fileName:", fileName);
    try {
      const response = await fetch(`data/highlight_result/${fileName}.json`);
      const data = await response.json();
      const { document_path, question, sub_query, sub_answers, chunks, final_answer } = data;



      if (document_path) {
        this.setState({
          url: document_path.trim(),
          // highlights: testHighlights[document_path] ? [...testHighlights[document_path]] : [],
          question: question || "",
          sub_query: sub_query || [],
          sub_answers: sub_answers || [],
          chunks: chunks || [],
          finalAnswer: final_answer || "",
        }, () => {
          this.highlightRetrievedTexts(chunks);
        });
      }
      
    } catch (error) {
      console.error("Error fetching document path:", error);
    }
  };

//   fetchJsonPath = async () => {
//     try {
//       // 使用相对路径读取本地 JSON 文件
//       const response = await fetch("data/highlight_result/result_20240628_115846.json");
//       const data = await response.json();
//       const { document_path, question, sub_query, sub_answers, retrieved_docs, final_answer } = data;

//       // console.log("document_path:", document_path);
//       // console.log("retrieved_docs:", retrieved_docs);

//       if (document_path) {
//         this.setState({
//           url: document_path.trim(),
//           // highlights: testHighlights[document_path] ? [...testHighlights[document_path]] : [],
//           question: question || "",
//           sub_query: sub_query || [],
//           sub_answers: sub_answers || [],
//           retrieved_docs: retrieved_docs || [],
//           finalAnswer: final_answer || "",
//         }, () => {
//           this.highlightRetrievedTexts(retrieved_docs);
//         });
        
//       }
      
//     } catch (error) {
//       console.error("Error fetching document path:", error);
//     }
    
// };


  highlightRetrievedTexts = async (chunks: Array<Array<string>>) => {
    const emoji_list = ["1🔍", "2👀", "3💩"]
    try {
      const pdf = await getDocument(this.state.url).promise;

      chunks.forEach(async (docArray, docArrayIndex) => { // for different sub_query's retrival
        // docArray.forEach(async (doc, docIndex) => { // for each retrieved chunk
        // console.log("doc:", doc[0]);
        
        let docTextOriginal = docArray[0]; // docText is a string
        let docText = docTextOriginal.replace(/[^a-zA-Z0-9]/g, '').toLocaleLowerCase();
        const docTextLength = docText.length;
        // console.log("docPage(From 0):", doc[1]);
        // let docPage = Number(doc[1])+1;
        // console.log("docPage(Number):", docPage);
        for (let i = 0; i < pdf.numPages; i++) {
          let docPage = i+1;
          let page = await pdf.getPage(i+1);
          const viewport = page.getViewport({ scale: 1 });
          let textContent = await page.getTextContent();
          let textItems = textContent.items;

          for (let i = 0; i < textItems.length; i++) {
            let candidate_text = textItems.slice(i).map(item => item.str).join('').replace(/[^a-zA-Z0-9]/g, '').slice(0, Math.min(docTextLength, textItems.length-i)).toLowerCase();
            if (candidate_text == docText) {
              const startIndex = i;
              console.log("For", docArray[1])
              console.log("START Match found at:", i);
              // console.log("candidate_text:", candidate_text);
              console.log("docTextOriginal:", docTextOriginal);
              // find the index of the last of candidate_text in textItems

              for (let j = textItems.length; j >= i; j--) {
                let candidate_text2 = textItems.slice(i, j).map(item => item.str).join('').replace(/[^a-zA-Z0-9]/g, '').slice(-docTextLength).toLowerCase();
                if (candidate_text2 == docText) {
                  const endIndex = j-1;
                  console.log("END Match found at:", j);

                  let highLightArea = this.getHighlightArea(startIndex, endIndex, textItems);
                  console.log("highlightArea:", highLightArea);
                  // this.getExistingHighlights();

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
                        pageNumber: docPage,
                      },
                      content: {
                        text: docTextOriginal,
                      },
                      comment: {
                        text: docArray[1],
                        emoji: docArray[1],
                      }
                    });
                  }

                  break;
                }
              }

              
              break;
            }
          }

        }
          // let page = await pdf.getPage(docPage);
          // const viewport = page.getViewport({ scale: 1 });
          // let textContent = await page.getTextContent();
          // let textItems = textContent.items;
          // console.log("textItems:", textItems);
          // let pageItem = textItems.map(item => item.str).join("\n");

          




        // });
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

  render() {
    const { url, highlights, question, sub_query, sub_answers, finalAnswer } = this.state;

    return (
      <div className="App" style={{ display: "flex", height: "100vh" }}>
        <Sidebar
          // highlights={highlights}
          // resetHighlights={this.resetHighlights}
          // toggleDocument={this.toggleDocument}
          question={question}
          sub_query={sub_query}
          sub_answers={sub_answers}
          finalAnswer={finalAnswer}
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
                            { image: screenshot(boundingRect) }
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


