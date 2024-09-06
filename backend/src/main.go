package main

import (
	"log"
	"os"

	"github.com/hotbrainy/go-leadopt/backend/controllers"
	"github.com/hotbrainy/go-leadopt/backend/db"
	"github.com/kataras/iris/v12"
	"github.com/kataras/iris/v12/mvc"
)

func main() {
	db := &db.Conn{}
	db.Init()

	app := iris.New()

	api := app.Party("/api")
	api.Use(iris.Compression)
	{
		profileAPI := api.Party("/profile")
		m := mvc.New(profileAPI)
		m.Handle(new(controllers.ProfileController))
	}

	port := (map[bool]string{true: "8081", false: os.Getenv("PORT")})[os.Getenv("PORT") == ""]

	if port == "" {
		log.Fatal("PORT environment variable not specified")
	}

	if err := app.Listen(":" + port); err != nil {
		log.Fatal(err)
	}
}
