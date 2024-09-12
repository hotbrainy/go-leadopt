"use client";

import { Alert, Input, Layout, Row, Typography } from "antd";
import { useWebSocket } from "next-ws/client";
import React, { useEffect, useState } from "react";

import Markdown from "react-markdown";

import remarkGfm from "remark-gfm";

// import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
// import { dark } from "react-syntax-highlighter/dist/esm/styles/prism";

const { Text } = Typography;
const { Content } = Layout;
const { Search } = Input;

interface MessageType {
  role: string;
  type?: string;
  content?:
    | string
    | { type?: string; format?: string; content?: string }
    | null;
  start?: boolean;
  end?: boolean;
  format?: string;
}
// const ws = new WebSocket("ws://127.0.0.1:8000");
const Queries: React.FC = () => {
  const mergeMessagesByRole = (data: MessageType[]) => {
    const merged: { role: string; type: string | undefined; content: any }[] =
      [];
    let currentRole: string = "";
    let currentType: string | undefined = "";
    let currentContent: unknown = "";

    data.forEach((msg) => {
      if (msg.content) {
        if (msg.role === currentRole && msg.type === currentType) {
          currentContent += msg.content.toString(); // Append content for the same role
        } else {
          if (currentRole !== null && currentType !== null) {
            merged.push({
              role: currentRole,
              type: currentType,
              content: currentContent,
            }); // Push merged content for the previous role
          }
          currentRole = msg.role;
          currentType = msg.type;
          currentContent = msg.content; // Start new content
        }
      } else if (msg.start || msg.end) {
        // merged.push(msg); // Push start/end markers
      }
    });

    if (currentContent) {
      merged.push({
        role: currentRole,
        type: currentType,
        content: currentContent,
      }); // Push the last merged content
    }

    return merged;
  };
  const [messages, setMessages] = useState<any[]>([]);
  const ws = useWebSocket();
  useEffect(() => {
    if (!ws) return;

    const handleOpen = () => {
      console.log("WebSocket connected");
      ws.send(
        JSON.stringify({
          auth: "dummy-api-key",
        })
      );
    };

    const handleMessage = async (event: MessageEvent) => {
      const payload =
        typeof event.data === "string" ? event.data : await event.data.text();
      const m = JSON.parse(payload) as MessageType;
      console.log({ m });
      setMessages((mm) => [...mm, m]);
    };

    const handleError = () => {
      console.log("WebSocket error");
    };

    const handleClose = () => {
      console.log("WebSocket closed");
    };
    ws.send(
      JSON.stringify({
        auth: "dummy-api-key",
      })
    );
    ws.addEventListener("open", handleOpen);
    ws.addEventListener("message", handleMessage);
    ws.addEventListener("error", handleError);
    ws.addEventListener("close", handleClose);

    return () => {
      ws.removeEventListener("open", handleOpen);
      ws.removeEventListener("message", handleMessage);
      ws.removeEventListener("error", handleError);
      ws.removeEventListener("close", handleClose);
    };
  }, [ws]);

  const onSearch = (v: string) => {
    if (ws?.readyState === WebSocket.OPEN) {
      const startBlock: MessageType = {
        role: "user",
        //"type": "message",
        start: true,
      };
      ws.send(JSON.stringify(startBlock));
      const messageBlock: MessageType = {
        role: "user",
        type: "message",
        content: v,
      };
      ws.send(JSON.stringify(messageBlock));
      const endBlock: MessageType = {
        role: "user",
        //"type": "message",
        end: true,
      };
      ws.send(JSON.stringify(endBlock));
      // setMessage([startBlock, messageBlock, endBlock]);
      setMessages([...messages, startBlock, messageBlock, endBlock]);
    } else {
      console.log("WebSocket is not open. Unable to send message.");
    }
  };

  const renderContent = () => {
    return mergeMessagesByRole(messages).map((message, index) =>
      message.role == "user" ? (
        <Row justify="end" key={index}>
          <Alert
            message={
              message.content?.content
                ? message.content.content
                : message.content
            }
          ></Alert>
        </Row>
      ) : (
        <Row key={index} justify="start">
          {/* <Markdown
            children={
              message.content &&
              (message.content?.content
                ? message.content.content
                : message.content)
            }
            components={{
              code(props) {
                const { children, className, node, ...rest } = props;
                const match = /language-(\w+)/.exec(className || "");
                return match ? (
                  <SyntaxHighlighter
                    {...rest}
                    PreTag="div"
                    children={String(children).replace(/\n$/, "")}
                    language={match[1]}
                    style={dark}
                  />
                ) : (
                  <code {...rest} className={className}>
                    {children}
                  </code>
                );
              },
            }}
          /> */}
          <Markdown key={index} remarkPlugins={[remarkGfm]}>
            {message.content &&
              (message.content?.content
                ? message.content.content
                : message.content)}
          </Markdown>
        </Row>
      )
    );
  };
  return (
    <Content className="relative mt-4 m-2 flex flex-col xs:mx-10 sm:mx-10 md:mx-32 gap-4 overflow-auto">
      <div className="h-[calc(100vh-140px)] overflow-auto">
        <Text>Hello, How can I help you today?</Text>
        {renderContent()}
      </div>
      {/*   <Row justify="end">
        <Alert message="Can you check the database is connected with my profile?"></Alert>
      </Row>
      <Text className="break-words">
        Yes, it was connected properly. Your database is MongoDB and it contains
        several databases. Do you want to get more detail about the database?
      </Text>

      <Row justify="end">
        <Alert message="Can you show me the database names?"></Alert>
      </Row> */}
      <Search
        placeholder="Ask something to the agent"
        allowClear
        enterButton="Send"
        size="large"
        onSearch={onSearch}
        className="w-full absolute bottom-2"
      />
    </Content>
  );
};

export default Queries;
