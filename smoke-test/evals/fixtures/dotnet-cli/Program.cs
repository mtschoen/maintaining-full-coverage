using System;
using System.IO;
using System.Text.Json;

namespace WordCounter;

class Program
{
    static int Main(string[] arguments)
    {
        if (arguments.Length == 0)
        {
            Console.Error.WriteLine("Usage: WordCounter <file>");
            return 1;
        }

        var filePath = arguments[0];
        if (!File.Exists(filePath))
        {
            Console.Error.WriteLine($"File not found: {filePath}");
            return 1;
        }

        var text = File.ReadAllText(filePath);
        var words = text.Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);

        Console.WriteLine($"Words: {words.Length}");
        Console.WriteLine($"Characters: {text.Length}");
        Console.WriteLine($"Lines: {text.Split('\n').Length}");

        return 0;
    }
}
