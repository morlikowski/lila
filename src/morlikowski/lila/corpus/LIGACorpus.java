package morlikowski.lila.corpus;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * https://github.com/llaisdy/liga
 * 
 * @author Matthias Orlikowski
 *
 */

public class LIGACorpus extends Corpus {

	@Override
	public void load(String datasetPath) {
		Path dataset = Paths.get(datasetPath);
		this.documents = new LinkedList<>();
		try (DirectoryStream<Path> languageDirectoriesStream = Files.newDirectoryStream(dataset)) {
			languageDirectoriesStream.forEach(this::readLanguageDirectory);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private void readLanguageDirectory(Path dir) {
		String language = dir.getFileName().toString();
		try (DirectoryStream<Path> languageFilesStream = Files.newDirectoryStream(dir)) {
			languageFilesStream.forEach(file -> this.readLanguageFile(file, language));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private void readLanguageFile(Path file, String label) {
		List<Document> documentsInFile = null;
		try (BufferedReader reader = Files.newBufferedReader(file)) {
			documentsInFile = reader.lines().map(line -> new Document(label, line)).collect(Collectors.toList());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		this.documents.addAll(documentsInFile);
	}

}
