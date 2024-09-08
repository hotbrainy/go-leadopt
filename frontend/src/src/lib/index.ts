"use server";

export const getData = () => {
  console.log(process.env.NEXT_PUBLIC_API_URL);
  return fetch(`http://${process.env.NEXT_PUBLIC_API_URL}/api/profile`).then(
    (res) => {
      return res.json();
    }
  );
};
