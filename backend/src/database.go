package main

import (
	"context"
)

type database interface {
	entries(context.Context) ([]leadoptEntry, error)
	addEntry(context.Context, leadoptEntry) error
}
