"use client";

import { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sparkles, Loader2 } from "lucide-react";
import {
  getExtractionSchemas,
  extractData,
  type ExtractionSchema,
} from "@/lib/api";

export default function ExtractionPage() {
  const [schemas, setSchemas] = useState<ExtractionSchema[]>([]);
  const [selectedSchema, setSelectedSchema] = useState<string>("");
  const [inputText, setInputText] = useState<string>("");
  const [extractedData, setExtractedData] = useState<Record<string, unknown> | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getExtractionSchemas().then((data) => {
      setSchemas(data);
      if (data.length > 0) {
        setSelectedSchema(data[0].id);
        setInputText(data[0].example_text);
      }
    });
  }, []);

  const handleSchemaChange = (schemaId: string) => {
    setSelectedSchema(schemaId);
    const schema = schemas.find((s) => s.id === schemaId);
    if (schema) {
      setInputText(schema.example_text);
    }
    setExtractedData(null);
    setError(null);
  };

  const handleExtract = async () => {
    if (!inputText.trim() || !selectedSchema) return;

    setIsLoading(true);
    setError(null);
    setExtractedData(null);

    try {
      const result = await extractData(inputText, selectedSchema);
      setExtractedData(result.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Extraction failed");
    } finally {
      setIsLoading(false);
    }
  };

  const selectedSchemaInfo = schemas.find((s) => s.id === selectedSchema);

  const renderValue = (value: unknown): React.ReactNode => {
    // Handle null/undefined
    if (value === null || value === undefined || value === "null") {
      return <span className="text-muted-foreground italic">Not provided</span>;
    }

    // Handle arrays
    if (Array.isArray(value)) {
      if (value.length === 0) {
        return <span className="text-muted-foreground italic">None</span>;
      }

      // Special rendering for labels/tags (short strings)
      const isLabels = value.every((item) => typeof item === "string" && item.length < 30);
      if (isLabels) {
        return (
          <div className="flex flex-wrap gap-1.5">
            {value.map((item, idx) => (
              <Badge key={idx} variant="secondary" className="text-xs">
                {String(item)}
              </Badge>
            ))}
          </div>
        );
      }

      // Regular list for longer items
      return (
        <ul className="space-y-1.5 list-disc list-inside">
          {value.map((item, idx) => (
            <li key={idx} className="text-sm">
              {String(item)}
            </li>
          ))}
        </ul>
      );
    }

    // Handle strings - check for multi-line content
    if (typeof value === "string") {
      const lines = value.split("\n").filter((line) => line.trim());
      if (lines.length > 3 || value.length > 200) {
        return (
          <div className="bg-muted/50 p-3 rounded border text-sm whitespace-pre-wrap font-mono">
            {value}
          </div>
        );
      }
      return <span className="font-medium">{value}</span>;
    }

    // Handle objects
    if (typeof value === "object") {
      return (
        <div className="bg-muted/50 p-3 rounded border">
          <pre className="text-xs font-mono overflow-x-auto">
            {JSON.stringify(value, null, 2)}
          </pre>
        </div>
      );
    }

    // Handle primitives
    return <span className="font-medium">{String(value)}</span>;
  };

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] p-6">
      <div className="w-full max-w-6xl">
        <Card className="shadow-sm">
          <CardHeader className="border-b py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Sparkles className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-lg font-semibold">
                  Structured Data Extraction
                </CardTitle>
              </div>
              {selectedSchemaInfo && (
                <Badge variant="secondary" className="text-xs">
                  {selectedSchemaInfo.category}
                </Badge>
              )}
            </div>
          </CardHeader>

          <div className="p-6 space-y-6">
            <div>
              <label className="text-sm font-medium mb-2 block">
                Extraction Type
              </label>
              <Select
                value={selectedSchema}
                onValueChange={handleSchemaChange}
                disabled={isLoading}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select extraction type" />
                </SelectTrigger>
                <SelectContent>
                  {schemas.map((schema) => (
                    <SelectItem key={schema.id} value={schema.id}>
                      <div className="flex flex-col items-start">
                        <span className="font-medium">{schema.name}</span>
                        <span className="text-xs text-muted-foreground">
                          {schema.description}
                        </span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">
                Input Text
              </label>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                disabled={isLoading}
                placeholder="Enter text to extract data from..."
                className="w-full min-h-[200px] p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring text-sm font-mono"
              />
            </div>

            <Button
              onClick={handleExtract}
              disabled={isLoading || !inputText.trim()}
              className="w-full"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Extracting...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 mr-2" />
                  Extract Data
                </>
              )}
            </Button>

            {error && (
              <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
                <p className="text-sm text-destructive font-medium">
                  Error: {error}
                </p>
              </div>
            )}

            {extractedData && (
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Extracted Data
                </label>
                <div className="bg-muted/30 border rounded-lg divide-y">
                  {Object.entries(extractedData).map(([key, value]) => (
                    <div key={key} className="p-4">
                      <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
                        {key.replace(/_/g, " ")}
                      </div>
                      <div className="text-sm">
                        {renderValue(value)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
