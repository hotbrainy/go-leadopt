"use client";

import {
  Affix,
  Alert,
  Button,
  Flex,
  Form,
  FormProps,
  Input,
  Layout,
  message,
  Row,
  Tooltip,
  FloatButton,
} from "antd";
import { useWebSocket } from "next-ws/client";
import React, { KeyboardEvent, useContext, useEffect, useState } from "react";

import {
  SendOutlined,
  EyeOutlined,
  EyeInvisibleOutlined,
} from "@ant-design/icons";
import Markdown from "react-markdown";

import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { BiArrowBack } from "react-icons/bi";
import { useRouter } from "next/navigation";

import api from "@/api";

import LayoutContext from "@/contexts/LayoutContextProvider";

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
// const ws = new WebSocket("ws://127.0.0.1:8000/");
const Message: React.FC = (props: any) => {
  const ws = useWebSocket();
  const router = useRouter();
  const layoutContext = useContext(LayoutContext);
  if (!layoutContext) {
    throw new Error("Component must be used within a LayoutContext Provider");
  }

  const { collapsed } = layoutContext;
  const [messages, setMessages] = useState<any[]>([]);

  const [form] = Form.useForm();
  const [serverStatus, setServerStatus] = useState<string>("complete");
  const [loading, setLoading] = useState<boolean>(false);
  const [showCode, setShowCode] = useState<boolean>(false);
  const [isAtBottom, setIsAtBottom] = useState<boolean>(false);
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

  const onSend = (prompt: string) => {
    if (ws?.readyState === WebSocket.OPEN) {
      setLoading(true);
      const startBlock: MessageType = {
        role: "user",
        //"type": "message",
        start: true,
      };
      ws.send(
        JSON.stringify({
          type: "interpreter",
          action: "chat",
          payload: startBlock,
        })
      );
      const messageBlock: MessageType = {
        role: "user",
        type: "message",
        content: prompt,
      };
      ws.send(
        JSON.stringify({
          type: "interpreter",
          action: "chat",
          payload: messageBlock,
        })
      );
      const endBlock: MessageType = {
        role: "user",
        //"type": "message",
        end: true,
      };
      ws.send(
        JSON.stringify({
          type: "interpreter",
          action: "chat",
          payload: endBlock,
        })
      );
      setMessages([...messages, startBlock, messageBlock, endBlock]);
    } else {
      console.log("WebSocket is not open. Unable to send message.");
    }
    form.resetFields();
  };
  const handleKeyUp = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (!e.shiftKey) {
      e.preventDefault();
      form.submit();
    }
  };
  const renderContent = () => {
    return messages && messages.length
      ? mergeMessagesByRole(messages).map((message, index) =>
          message.role == "user" ? (
            <Row justify="end" key={index} className="my-5">
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
            <Row
              key={index}
              justify="start"
              className={`mt-1 block ${
                (message.type === "code" || message.type === "console") &&
                !showCode
                  ? "hidden"
                  : ""
              }`}
            >
              <Markdown
                remarkPlugins={[remarkGfm]}
                className={`prose lg:prose-xl dark:prose-invert`}
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
                          margin: 0,
                          display: showCode ? "inherit" : "none",
                        }}
                        showInlineLineNumbers
                        showLineNumbers
                        wrapLongLines
                      >
                        {String(children).replace(/\n$/, "")}
                      </SyntaxHighlighter>
                    ) : (
                      <code
                        {...rest}
                        className={`${className}`}
                      >
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
        )
      : null;
  };

  const onFinish: FormProps<any>["onFinish"] = (values) => {
    onSend(values.prompt);
  };

  const onFinishFailed: FormProps<any>["onFinishFailed"] = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  const onBack = () => {
    router.push("/home");
  };
  useEffect(() => {
    if (!ws) return;

    const handleOpen = () => {
      console.log("WebSocket connected");
      ws.send(
        JSON.stringify({
          type: "auth",
          auth: "dummy-api-key",
          token:
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2ODE1Mjk0LCJpYXQiOjE3MjY4MDQ0OTQsImp0aSI6ImZhMmQ1MzdkMjE1ZTQzM2FiMzQ4NTFmZjU5MWMzMzY2IiwidXNlcl9pZCI6MX0.LQWpe3g3YwUtdVImqjuUTtSovghJFAcLM2lx5bPbF3Y",
        })
      );
    };

    const handleMessage = async (event: MessageEvent) => {
      const payload =
        typeof event.data === "string" ? event.data : await event.data.text();
      const data = JSON.parse(payload);
      if (data.type == "auth") {
        ws.send(
          JSON.stringify({
            type: "interpreter",
            action: "init",
            session_id: props.params.id,
          })
        );
      }
      if(data?.payload?.end){
        setLoading(false);
      }
      if(data?.payload?.start){
        setLoading(true);
      }
      if (data.type == "interpreter" && data.action == "chat") {
        if (data.role == "server" && data.type == "status" && data.content) {
          setServerStatus(data.content.toString());
        }

        setMessages((mm) => [...mm, data.payload]);
      }
    };

    const handleError = (err: Event) => {
      console.log({ err });
      message.error("WebSocket Error!");
      console.log("WebSocket error");
    };

    const handleClose = () => {
      message.warning("WebSocket closed!");
      console.log("WebSocket closed");
    };
    ws.addEventListener("open", handleOpen);
    ws.addEventListener("message", handleMessage);
    ws.addEventListener("error", handleError);
    ws.addEventListener("close", handleClose);

    setTimeout(() => {
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(
          JSON.stringify({
            type: "auth",
            token:
              "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2ODE1Mjk0LCJpYXQiOjE3MjY4MDQ0OTQsImp0aSI6ImZhMmQ1MzdkMjE1ZTQzM2FiMzQ4NTFmZjU5MWMzMzY2IiwidXNlcl9pZCI6MX0.LQWpe3g3YwUtdVImqjuUTtSovghJFAcLM2lx5bPbF3Y",
          })
        );
      }
    }, 100);
    return () => {
      ws.removeEventListener("open", handleOpen);
      ws.removeEventListener("message", handleMessage);
      ws.removeEventListener("error", handleError);
      ws.removeEventListener("close", handleClose);
    };
  }, [ws, props.params.id]);

  useEffect(() => {
    api(`interpreter/sessions/${props.params.id}/messages/all`).then((res) => {
      setMessages(res);
    });
    setIsAtBottom(false);
  }, [props.params.id]);
  return (
    <Content className="relative mt-2 max-h-[calc(100vh-130px)]  flex flex-col gap-4 overflow-auto ">
      <FloatButton
        className={`fixed top-[80px] ${
          collapsed
            ? "left-[20px] md:left-[100px]"
            : "left-[20px] md:left-[220px]"
        }`}
        icon={<BiArrowBack />}
        onClick={onBack}
      ></FloatButton>
      <div className="px-4 md:px-20 lg:px-40 xl:px-80">
        {/*   <Scrollbar
        ref={scrollbar}
        plugins={{
          overscroll: {
            effect: OverscrollEffect.BOUNCE,
          },
        }}
        onScroll={onScroll}
        className="px-4 md:px-10"
      > */}
        {renderContent()}
        <div className="w-full h-20"></div>
        {isAtBottom && (
          <FloatButton
            className={`bottom-16 fixed ${
              collapsed ? "left-[calc(50%+40px)]" : "left-[calc(50%+100px)]"
            }`}
          >
            New chat
          </FloatButton>
        )}
        {/* </Scrollbar> */}
      </div>
      <Affix
        offsetBottom={0}
        className={`bottom-0 fixed ${
          collapsed
            ? "left-[20px] md:left-[100px] w-[calc(100%-40px)] md:w-[calc(100%-120px)]"
            : "left-[20px] md:left-[250px] w-[calc(100%-40px)] md:w-[calc(100%-300px)]"
        } `}
      >
        {/* {waitingApprove ? (
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
        ) : null} */}
        <Form
          form={form}
          name="promptForm"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          autoComplete="off"
        >
          <Flex className="w-full relative align-bottom justify-end items-end flex flex-row">
            <Form.Item
              name="prompt"
              rules={[
                { required: true /*  message: "Please input your prompt!" */ },
              ]}
              className="w-full"
            >
              <Input.TextArea
                autoSize
                placeholder="Ask something to the agent"
                className="w-full border-none focus:shadow-none"
                onPressEnter={handleKeyUp}
                size="large"
              />
            </Form.Item>
            <Flex gap={2}>
              <Form.Item>
                <Tooltip title="Send prompt">
                  <Button
                    size="large"
                    type="primary"
                    loading={loading || serverStatus != "complete"}
                    htmlType="submit"
                  >
                    <SendOutlined />
                  </Button>
                </Tooltip>
              </Form.Item>
              <Form.Item>
                <Tooltip title="Show Code">
                  <Button
                    size="large"
                    type="primary"
                    icon={showCode ? <EyeInvisibleOutlined /> : <EyeOutlined />}
                    onClick={() => setShowCode(!showCode)}
                  ></Button>
                </Tooltip>
              </Form.Item>
            </Flex>
          </Flex>
        </Form>
      </Affix>
    </Content>
  );
};

export default Message;
