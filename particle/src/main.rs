#![allow(dead_code)]
#![allow(unused_imports)]
#![allow(unused_variables)]

mod grid;
mod particle;

use grid::Grid;
use particle::Particle;

use sdl2::event::Event;
use sdl2::keyboard::Keycode;
use sdl2::mouse::{MouseButton, MouseState};
use sdl2::pixels::Color;
use sdl2::rect::Rect;
use sdl2::render::Canvas;
use sdl2::video::Window;

const WINW: u32 = 800;
const WINH: u32 = 600;

struct GameState {
    grid: Grid<Particle>,
    curr: Option<Particle>,
}

fn main() -> Result<(), String> {
    let args: Vec<String> = std::env::args().collect();
    let (pixel_size, brush_size, update_count) = {
        if args.len() != 4 {
            (5, 5, 1)
        } else {
            (
                args[1].parse::<u32>().unwrap(),
                args[2].parse::<i32>().unwrap(),
                args[3].parse::<u32>().unwrap(),
            )
        }
    };
    let cursor_size = (2 * brush_size + 1) as u32 * pixel_size;
    
    let sdl_context = sdl2::init()?;
    let video_subsystem = sdl_context.video()?;

    let window = video_subsystem
        .window("particle", WINW, WINH)
        .position_centered()
        .build()
        .map_err(|e| e.to_string())?;

    let mut canvas = window
        .into_canvas()
        .accelerated()
        .build()
        .map_err(|e| e.to_string())?;
    println!("{:#?}", canvas.info());

    sdl_context.mouse().show_cursor(false);
    let mut event_pump = sdl_context.event_pump()?;
    let mut game_state = GameState {
        curr: None,
        grid: Grid::<Particle>::new((WINW / pixel_size) as usize, (WINH / pixel_size) as usize),
    };

    'main: loop {
        let start_time = std::time::Instant::now();

        for event in event_pump.poll_iter() {
            match event {
                Event::Quit { .. } |
                Event::KeyDown { keycode: Some(Keycode::Escape), .. } => {
                    break 'main;
                },
                Event::MouseButtonDown { mouse_btn: MouseButton::Right, .. } => {
                    game_state.curr = match game_state.curr {
                        Some(Particle::Sand)  => Some(Particle::Water),
                        Some(Particle::Water) => Some(Particle::Wall),
                        Some(Particle::Wall)  => Some(Particle::Sand),
                        _ => Some(Particle::Sand),
                    };

                    println!("brush: {:?}", game_state.curr);
                },
                Event::MouseButtonDown { mouse_btn: MouseButton::Middle, .. } => {
                    game_state.curr = None;
                    println!("brush: {:?}", game_state.curr);
                },
                _ => ()
            }
        }

        let mouse_state  = event_pump.mouse_state();
        let (left, x, y) = (mouse_state.left(), mouse_state.x(), mouse_state.y());
        if left {
            let (x, y) = (x / pixel_size as i32,y / pixel_size as i32);

            for dx in -brush_size..brush_size {
                for dy in -brush_size..brush_size {
                    if let Some(index) = game_state.grid.get_index((x + dx) as usize, (y + dy) as usize) {
                        game_state.grid.data[index] = match game_state.curr {
                            Some(particle) => particle,
                            None => Particle::Empty,
                        };
                    }
                }
            }
        }

        canvas.set_draw_color(Color::RGB(0, 0, 0));
        canvas.clear();
        game_state.grid.iter().enumerate().try_for_each(|(i, particle)| {
            match particle.color() {
                Some(color) => {
                    let (x, y) = game_state.grid.get_coords(i).unwrap();
                    let (x, y) = (x as i32, y as i32);
    
                    canvas.set_draw_color(color);
                    canvas.fill_rect(Rect::new(x * pixel_size as i32, y * pixel_size as i32, pixel_size, pixel_size))
                },
                None => Ok(())
            }
        })?;
        canvas.set_draw_color(Color::RGB(255, 255, 255));
        canvas.fill_rect(Rect::from_center((x, y), cursor_size, cursor_size))?;
        canvas.present();

        for _ in 0..update_count {
            let mut grid_copy = game_state.grid.clone();
            game_state.grid.iter().enumerate().for_each(|(i, particle)| {
                let (x, y) = game_state.grid.get_coords(i).unwrap();
                let (x, y) = (x as i32, y as i32);
        
                particle.update(x, y, &mut grid_copy)
            });
            game_state.grid = grid_copy;
        }
    }

    Ok(())
}