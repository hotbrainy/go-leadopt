"use client";

import {
  Affix,
  Alert,
  Button,
  Flex,
  Input,
  Layout,
  Row,
  Spin,
  Tooltip,
} from "antd";
import { useWebSocket } from "next-ws/client";
import React, { KeyboardEvent, useEffect, useState } from "react";
import {
  SendOutlined,
  CodeOutlined,
  EyeOutlined,
  LoadingOutlined,
  EyeInvisibleOutlined,
} from "@ant-design/icons";
import Markdown from "react-markdown";

import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

const { Content } = Layout;

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
  const ws = useWebSocket();
  const mergeMessagesByRole = (data: MessageType[]) => {
    const merged: {
      role: string;
      type: string | undefined;
      format: string | undefined;
      content: any;
    }[] = [];
    let currentRole: string = "";
    let currentType: string | undefined = "";
    let currentContent: unknown = "";
    let currentFormat: string | undefined = "";
    data
      .filter(
        (d) => d.content && d.format != "active_line" && d.role != "server"
      )
      .forEach((msg) => {
        if (msg.role !== "server" && msg.content) {
          if (msg.role === currentRole && msg.type === currentType) {
            if (msg.format !== "active_line")
              currentContent += msg.content.toString(); // Append content for the same role
          } else {
            if (currentRole !== null && currentType !== null) {
              merged.push({
                role: currentRole,
                type: currentType,
                format:
                  currentType == "console" && currentFormat !== "active_line"
                    ? "bash"
                    : currentFormat,
                content: currentContent,
              }); // Push merged content for the previous role
            }
            currentRole = msg.role;
            currentType = msg.type;
            currentFormat = msg.format;
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
        format:
          currentType == "console" && currentFormat !== "active_line"
            ? "bash"
            : currentFormat,
      }); // Push the last merged content
    }
    return merged;
  };
  const [messages, setMessages] = useState<any[]>([]);
  const [serverStatus, setServerStatus] = useState<string>("complete");
  const [loading, setLoading] = useState<boolean>(false);
  const [prompt, setPrompt] = useState<string>("");
  const [showCode, setShowCode] = useState<boolean>(false);
  const [waitingApprove, setWaitingApprove] = useState<boolean>(false);
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
      setLoading(false);
      if (m.role == "server" && m.type == "status" && m.content) {
        setServerStatus(m.content.toString());
      }
      if (m.role !== "server" && m.type == "code") {
        setWaitingApprove(true);
      }
      setMessages((mm) => [...mm, m]);
    };

    const handleError = () => {
      console.log("WebSocket error");
    };

    const handleClose = () => {
      console.log("WebSocket closed");
    };
    setTimeout(() => {
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(
          JSON.stringify({
            auth: "dummy-api-key",
          })
        );
      }
    }, 500);
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

  const onApproveCode = () => {
    const startCommandBlock = {
      role: "user",
      type: "command",
      start: true,
    };
    ws?.send(JSON.stringify(startCommandBlock));

    const commandBlock = {
      role: "user",
      type: "command",
      content: "go",
    };
    ws?.send(JSON.stringify(commandBlock));

    const endCommandBlock = {
      role: "user",
      type: "command",
      end: true,
    };
    ws?.send(JSON.stringify(endCommandBlock));
    setWaitingApprove(false);
  };
  const onPromptInput = (v: any) => {
    setPrompt(v.target.value);
  };
  const onSend = () => {
    if (ws?.readyState === WebSocket.OPEN) {
      setLoading(true);
      const startBlock: MessageType = {
        role: "user",
        //"type": "message",
        start: true,
      };
      ws.send(JSON.stringify(startBlock));
      const messageBlock: MessageType = {
        role: "user",
        type: "message",
        content: prompt,
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
      setPrompt("");
    } else {
      console.log("WebSocket is not open. Unable to send message.");
    }
  };
  const handleKeyUp = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (!e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };
  const renderContent = () => {
    return mergeMessagesByRole(messages).map((message, index) =>
      message.role == "user" ? (
        <Row justify="end" key={index} className="mt-1">
          <Alert
            className="lg:text-xl"
            message={
              message.content?.content
                ? message.content.content
                : message.content
            }
          ></Alert>
        </Row>
      ) : (
        <Row key={index} justify="start" className="mt-1 block">
          <Markdown
            remarkPlugins={[remarkGfm]}
            className={`prose lg:prose-xl dark:prose-invert ${
              (message.type === "code" || message.type === "console") &&
              !showCode
                ? "hidden"
                : ""
            }`}
            components={{
              code(props) {
                const { children, className, ...rest } = props;
                const match = /language-(\w+)/.exec(className || "");
                return match ? (
                  <SyntaxHighlighter
                    PreTag="span"
                    language={match[1]}
                    style={vscDarkPlus}
                    customStyle={{
                      padding: "none !important",
                      display: showCode ? "inline" : "none",
                    }}
                    showInlineLineNumbers
                    showLineNumbers
                    wrapLongLines
                  >
                    {String(children).replace(/\n$/, "")}
                  </SyntaxHighlighter>
                ) : (
                  <code {...rest} className={className}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content &&
              (message.type === "code" || message.type === "console"
                ? `\`\`\`\`${message.format}\n`
                : "") +
                (message.content?.content
                  ? message.content.content
                  : message.content) +
                (message.type === "code" || message.type === "console"
                  ? `\n\`\`\`\``
                  : "")}
          </Markdown>
        </Row>
      )
    );
  };
  return (
    <Content className="relative mt-4 m-2 pb-4 flex flex-col xs:mx-6 sm:mx-6 md:mx-14 gap-4 overflow-auto">
      <div className="min-h-[calc(100vh-160px)] overflow-auto pb-8">
        {renderContent()}
      </div>
      <Affix offsetBottom={10} className="bottom-2 absolute w-full">
        {waitingApprove ? (
          <Alert
            showIcon
            message="Waiting approve code..."
            icon={<Spin indicator={<LoadingOutlined spin />} size="small" />}
            action={
              <Button
                type="primary"
                disabled={
                  loading ||
                  (serverStatus !== "complete" &&
                    serverStatus !== "waiting_approve")
                }
                onClick={onApproveCode}
                icon={<CodeOutlined />}
              >
                Approve Code
              </Button>
            }
          ></Alert>
        ) : null}
        <Flex className="w-full relative p-1 align-bottom justify-end items-end flex flex-row">
          <Input.TextArea
            autoSize
            placeholder="Ask something to the agent"
            value={prompt}
            className="border-none focus:shadow-none"
            onChange={onPromptInput}
            onPressEnter={handleKeyUp}
          />
          <Flex gap={2}>
            <Tooltip title="Send prompt">
              <Button
                type="primary"
                disabled={prompt == ""}
                loading={loading || serverStatus != "complete"}
                onClick={onSend}
              >
                <SendOutlined />
              </Button>
            </Tooltip>
            <Tooltip title="Show Code">
              <Button
                type="primary"
                disabled={
                  loading ||
                  (serverStatus !== "complete" &&
                    serverStatus !== "waiting_approve")
                }
                icon={showCode ? <EyeInvisibleOutlined /> : <EyeOutlined />}
                onClick={() => setShowCode(!showCode)}
              ></Button>
            </Tooltip>
          </Flex>
        </Flex>
      </Affix>
    </Content>
  );
};

export default Queries;
