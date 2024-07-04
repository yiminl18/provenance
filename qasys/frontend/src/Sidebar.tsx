import React, { useState } from "react";
// import type { IHighlight } from "./react-pdf-highlighter";

interface Props {
  // highlights: Array<IHighlight>;
  // resetHighlights: () => void;
  // toggleDocument: () => void;
  question: string;
  sub_query: Array<string>;
  sub_answers: Array<string>;
  finalAnswer: string;
  onFileSubmit: (fileName: string) => void;
}

// const updateHash = (highlight: IHighlight) => {
//   document.location.hash = `highlight-${highlight.id}`;
// };

declare const APP_VERSION: string;

export function Sidebar({
  // highlights,
  // toggleDocument,
  // resetHighlights,
  question,
  sub_query,
  sub_answers,
  finalAnswer,
  onFileSubmit,
}: Props) {
  const [fileName, setFileName] = useState("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFileName(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onFileSubmit(fileName);
  };
  return (
    <div className="sidebar" style={{ width: "25vw", overflowY: "auto" }}>
      {/* <div className="description" style={{ padding: "1rem" }}>
        <h2 style={{ marginBottom: "1rem" }}>
          react-pdf-highlighter {APP_VERSION}
        </h2>
        <p>
          <small>
            To create area highlight hold ⌥ Option key (Alt), then click and
            drag.
          </small>
        </p>
      </div> */}

      {/* <ul className="sidebar__highlights">
        {highlights.map((highlight, index) => (
          <li
            key={index}
            className="sidebar__highlight"
            onClick={() => {
              updateHash(highlight);
            }}
          >
            <div>
              <strong>{highlight.comment.text}</strong>
              {highlight.content.text ? (
                <blockquote style={{ marginTop: "0.5rem" }}>
                  {`${highlight.content.text.slice(0, 90).trim()}…`}
                </blockquote>
              ) : null}
              {highlight.content.image ? (
                <div
                  className="highlight__image"
                  style={{ marginTop: "0.5rem" }}
                >
                  <img src={highlight.content.image} alt={"Screenshot"} />
                </div>
              ) : null}
            </div>
            <div className="highlight__location">
              Page {highlight.position.pageNumber}
            </div>
          </li>
        ))}
      </ul> */}
      <form onSubmit={handleSubmit} style={{ padding: "1rem" }}>
        <input
          type="text"
          value={fileName}
          onChange={handleInputChange}
          placeholder="Enter JSON file name"
        />
        <button type="submit">Submit</button>
      </form>

      <div className="sidebar__question" style={{ padding: "1rem" }}>
      <h3>Question</h3>
      <p>{question}</p>
      </div>

      <div className="sidebar__sub-query" style={{ padding: "1rem" }}>
        <h3>Sub Querys</h3>
        <ul>
          {sub_query.map((query, index) => (
            <li key={index}>{query}</li>
          ))}
        </ul>
      </div>

      <div className="sidebar__sub-answers" style={{ padding: "1rem" }}>
        <h3>Sub Answers</h3>
        <ul>
          {sub_answers.map((answer, index) => (
            <li key={index}>{answer}</li>
          ))}
        </ul>
      </div>

      <div className="sidebar__final-answer" style={{ padding: "1rem" }}>
        <h3>Final Answer</h3>
        <p>{finalAnswer}</p>
      </div>

      {/* <div style={{ padding: "1rem" }}>
        <button onClick={toggleDocument}>Toggle PDF document</button>
      </div> */}

      {/* {highlights.length > 0 ? (
        <div style={{ padding: "1rem" }}>
          <button onClick={resetHighlights}>Reset highlights</button>
        </div>
      ) : null} */}
    </div>
  );
}
