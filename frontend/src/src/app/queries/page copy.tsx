"use client";

import { Alert, Input, Layout, Row, Typography } from "antd";
import React, { useState } from "react";

import { useWebSocket } from "next-ws/client";

const { Text } = Typography;
const { Content } = Layout;
const { Search } = Input;

const Queries: React.FC = () => {
  const ws = useWebSocket();
  const [messages, setMessages] = useState<string[]>([]);
  console.log(messages);
  async function onMessage(event: MessageEvent) {
    console.log({ event });
    const payload =
      typeof event.data === "string" ? event.data : await event.data.text();
    const message = JSON.parse(payload);
    setMessages((p) => [...p, message]);
  }
  if (ws) {
    console.log(ws.readyState);
    if (ws.readyState == 3)
      ws.send(
        JSON.stringify({
          auth: "dummy-api-key",
        })
      );
  }

  ws?.addEventListener("message", onMessage);

  const onSearch = (v: unknown) => {
    console.log(v);

    ws?.send(
      JSON.stringify({
        role: "user",
        //"type": "message",
        start: true,
      })
    );

    ws?.send(
      JSON.stringify({
        role: "user",
        type: "message",
        content: v,
      })
    );

    ws?.send(
      JSON.stringify({
        role: "user",
        //"type": "message",
        end: true,
      })
    );
  };
  return (
    <Content className="relative mt-4 m-2 flex flex-col xs:mx-10 sm:mx-10 md:mx-32 gap-4">
      <Text>Hello, How can I help you today?</Text>
      <Row justify="end">
        <Alert message="Can you check the database is connected with my profile?"></Alert>
      </Row>
      <Text className="break-words">
        Yes, it was connected properly. Your database is MongDB and it contains
        several databases. Do you want to get more detail about the database?
      </Text>

      <Row justify="end">
        <Alert message="Can you show me the database names?"></Alert>
      </Row>
      <Search
        placeholder="Ask something to agent"
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
