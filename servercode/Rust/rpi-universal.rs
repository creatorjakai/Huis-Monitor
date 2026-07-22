use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};

const PORT: u16 = 5000;
const SERVER_PASSWORD: &str = "11223344";

fn handle_client(mut stream: TcpStream) {
    println!("Nieuwe client verbonden.");

    let mut reader = BufReader::new(stream.try_clone().unwrap());

    let mut password = String::new();

    if reader.read_line(&mut password).is_err() {
        return;
    }

    password = password.trim().to_string();

    if password != SERVER_PASSWORD {
        let _ = stream.write_all(b"LOGIN_FAILED\n");
        return;
    }

    let _ = stream.write_all(b"LOGIN_OK\n");

    loop {
        let mut message = String::new();

        match reader.read_line(&mut message) {
            Ok(0) => break,
            Ok(_) => {
                println!("{}", message.trim());

                let _ = stream.write_all(
                    b"Raspberry PI server zegt: Hallo!\n"
                );
            }
            Err(_) => break,
        }
    }

    println!("Client verbroken.");
}

fn main() {
    let listener = TcpListener::bind(("0.0.0.0", PORT))
        .expect("Kan poort niet openen");

    println!("SERVER GESTART op poort {}", PORT);

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => handle_client(stream),
            Err(e) => println!("Fout: {}", e),
        }
    }
}
