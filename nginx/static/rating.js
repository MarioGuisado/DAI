
document.addEventListener('DOMContentLoaded', () => {
    const span_para_estrellas = document.querySelectorAll('span.sp')

    span_para_estrellas.forEach((ele) => {
        ele.innerHTML = `
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
        `

        const stars = ele.querySelectorAll('.fa-star')

        stars.forEach((star, index) => {
            star.addEventListener('mouseover', () => {
                for (let i = 0; i <= index; i++) {
                    stars[i].classList.add('checked')
                }
            })

            star.addEventListener('mouseout', () => {
                for (let i = 0; i <= index; i++) {
                    stars[i].classList.remove('checked')
                }
            })

            star.addEventListener('click', () => {
                const productId = ele.dataset.id;
                puntuacion = index + 1;  

                let ratingStr = ele.dataset.rating.replace(/'/g, '"');
                let rating_ = JSON.parse(ratingStr);

                let url = `http://localhost:8000/etienda/api/productos/${productId}`;

                puntuacion_media = ((rating_.puntuación * rating_.cuenta) + puntuacion) / (rating_.cuenta + 1);
                puntuacion_media = puntuacion_media.toFixed(1);

                rating = {
                    "rate": puntuacion_media, 
                    "count": rating_.cuenta + 1
                }

                let payload = {
                    title: ele.dataset.nombre,
                    price: ele.dataset.precio,
                    description: ele.dataset.descripcion,
                    category: ele.dataset.categoria,
                    rating
                };

                fetch(url, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                })
                .then(response => {
                    console.log(response);
                    return response.json();
                })
                    .then(data => {
                        console.log(data);
                        location.reload();
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });

            })

        })
    })
})

