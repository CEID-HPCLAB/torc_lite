
#include <stdio.h>
#include <math.h>
#include <torc.h>

#define NTASKS 4

void slave(double *x, double *y)
{
    *y = sqrt(*x);

    printf("Rank %d: sqrt(%f) = %f\n",
           torc_node_id(), *x, *y);
}

int main(int argc, char **argv)
{
    double input[NTASKS];
    double result[NTASKS];

    int quantities[2] = {1, 1};

    MPI_Datatype datatypes[2] = {
        MPI_DOUBLE,
        MPI_DOUBLE
    };

    int callways[2] = {
        CALL_BY_COP,
        CALL_BY_RES
    };

    torc_register_task((void *)slave);

    if (torc_init(argc, argv, MODE_MS) != 0)
        return 0;

    for (int i = 0; i < NTASKS; i++) {

        input[i] = (double)(i + 1);
        result[i] = -1.0;

        void *addresses[2] = {
            &input[i],
            &result[i]
        };

        torc_create_packed(
            -1,
            (void (*)())slave,
            2,
            quantities,
            datatypes,
            callways,
            addresses);
    }

    torc_waitall();

    for (int i = 0; i < NTASKS; i++)
        printf("Result[%d] = %f\n", i, result[i]);

    torc_finalize();

    return 0;
}
